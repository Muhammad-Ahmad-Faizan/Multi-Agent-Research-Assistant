from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
import asyncio
import json
import logging

from app.graph.build_graph import build_graph
from app.graph.state import initial_state
from app.models import RunStatusResponse

router = APIRouter(prefix="/research", tags=["research"])
logger = logging.getLogger(__name__)

# In-memory store for demo purposes
active_runs = {}

# Compile the graph with interrupts
graph = build_graph(interrupt=True)

class ResearchRequest(BaseModel):
    question: str

class ApprovePlanRequest(BaseModel):
    approved: bool
    edited_plan: Optional[List[str]] = None

@router.post("", response_model=RunStatusResponse)
async def start_research(req: ResearchRequest):
    run_id = str(uuid.uuid4())
    state = initial_state(req.question, run_id)
    
    config = {"configurable": {"thread_id": run_id}}
    active_runs[run_id] = config
    
    # Run graph async until the interrupt point
    async for s in graph.astream(state, config=config):
        pass
            
    current_state = graph.get_state(config).values
    
    return RunStatusResponse(
        run_id=run_id,
        status=current_state.get("status", "error"),
        plan=current_state.get("plan", []),
        current_subquestion_index=current_state.get("current_subquestion_index", 0),
        findings_count=len(current_state.get("findings", [])),
        report=current_state.get("report"),
        error_message=current_state.get("error_message")
    )

@router.get("/{run_id}/status", response_model=RunStatusResponse)
async def get_status(run_id: str):
    if run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found")
        
    config = active_runs[run_id]
    current_state = graph.get_state(config).values
    
    return RunStatusResponse(
        run_id=run_id,
        status=current_state.get("status", "error"),
        plan=current_state.get("plan", []),
        current_subquestion_index=current_state.get("current_subquestion_index", 0),
        findings_count=len(current_state.get("findings", [])),
        report=current_state.get("report"),
        error_message=current_state.get("error_message")
    )

@router.post("/{run_id}/approve-plan")
async def approve_plan(run_id: str, req: ApprovePlanRequest):
    if run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found")
        
    config = active_runs[run_id]
    current_state = graph.get_state(config).values
    
    if current_state.get("status") != "awaiting_approval":
        raise HTTPException(status_code=400, detail="Run is not awaiting approval")
        
    if not req.approved:
        graph.update_state(config, {"status": "cancelled"})
        return {"status": "cancelled"}
        
    update = {"plan_approved": True}
    if req.edited_plan is not None:
        update["plan"] = req.edited_plan
        
    graph.update_state(config, update)
    
    # Resume graph execution in the background
    async def resume_graph():
        try:
            async for _ in graph.astream(None, config=config):
                pass
        except Exception as e:
            logger.error(f"Error resuming graph: {e}")
            graph.update_state(config, {"status": "error", "error_message": str(e)})
            
    asyncio.create_task(resume_graph())
    
    return {"status": "resumed"}

@router.get("/{run_id}/stream")
async def stream_progress(run_id: str):
    if run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found")
        
    config = active_runs[run_id]
    
    async def event_generator():
        last_status = None
        last_subq = -1
        
        while True:
            current_state = graph.get_state(config).values
            current_status = current_state.get("status")
            current_subq = current_state.get("current_subquestion_index", 0)
            
            if current_status != last_status or current_subq != last_subq:
                msg = ""
                if current_status == "researching":
                    total_subq = len(current_state.get("plan", []))
                    msg = f"Researching sub-question {current_subq + 1} of {total_subq}..."
                elif current_status == "analyzing":
                    msg = "Analyzing findings..."
                elif current_status == "complete":
                    msg = "Report complete!"
                elif current_status == "error":
                    msg = "An error occurred."
                elif current_status == "cancelled":
                    msg = "Run cancelled."
                    
                if msg:
                    yield f"data: {json.dumps({'node': current_status, 'message': msg})}\n\n"
                    
                last_status = current_status
                last_subq = current_subq
                
            if current_status in ["complete", "error", "cancelled"]:
                break
                
            await asyncio.sleep(1.0)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{run_id}/trace")
async def get_trace(run_id: str):
    if run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found")
        
    config = active_runs[run_id]
    history = list(graph.get_state_history(config))
    trace = []
    
    for state_snap in reversed(history):
        state = state_snap.values
        node = getattr(state_snap, "next", ["unknown"])[0] if getattr(state_snap, "next", None) else "END"
        
        status = state.get('status')
        summary = f"Transition to {node} | Status: {status}"
        
        if status == "researching":
            summary = f"Researching subquestion {state.get('current_subquestion_index', 0) + 1}"
        elif status == "analyzing":
            summary = f"Analyzed findings, needs more: {state.get('needs_more_research')}"
            
        trace.append({
            "timestamp": getattr(state_snap, "created_at", ""),
            "node": node,
            "summary": summary
        })
        
    return {"trace": trace}
