from pydantic import BaseModel, Field
from typing import List, Dict
import logging
import json

from app.graph.state import ResearchState
from app.graph.llm import get_chat_model
from app.tools.web_search import search_web
from app.config import settings

logger = logging.getLogger(__name__)

class ResearchPlan(BaseModel):
    sub_questions: List[str] = Field(
        description="Specific, non-overlapping sub-questions that collectively cover the original question. Avoid vague or duplicate sub-questions."
    )

def planner_node(state: ResearchState) -> dict:
    """
    Takes the original question and breaks it down into specific, 
    researchable sub-questions.
    """
    logger.info(f"run={state.get('run_id')} node=planner status=started")
    question = state["original_question"]
    llm = get_chat_model()
    structured_llm = llm.with_structured_output(ResearchPlan)
    
    prompt = (
        "You are an expert research planner. Break down the user's original question into 3-5 specific, "
        "researchable sub-questions. Generate sub-questions that are non-overlapping in CONTENT, not just phrasing. "
        "Each sub-question should probe a genuinely distinct facet of the topic — for example: a specific technique or mechanism, "
        "production/deployment considerations, evaluation or measurement methods, trade-offs or limitations, and comparative alternatives. "
        "Do not generate two sub-questions that would be answered by the same source material.\n\n"
        f"Original Question: {question}"
    )
    
    result = structured_llm.invoke(prompt)
    logger.info(f"run={state.get('run_id')} node=planner status=finished subquestions={len(result.sub_questions)}")
    
    return {
        "plan": result.sub_questions,
        "status": "awaiting_approval"
    }

async def researcher_node(state: ResearchState) -> dict:
    """
    Calls the Tavily search tool for the current sub-question and 
    appends the results to the research results.
    """
    plan = state.get("plan", [])
    idx = state.get("current_subquestion_index", 0)
    
    if idx >= len(plan):
        logger.warning(f"run={state.get('run_id')} node=researcher status=skipped reason='No more sub-questions'")
        return {}
        
    sub_question = plan[idx]
    logger.info(f"run={state.get('run_id')} node=researcher status=started subquestion={idx+1}/{len(plan)}")
    
    results = await search_web(sub_question)
    
    # Tag results with the subquestion they came from
    for r in results:
        r["subquestion"] = sub_question
        
    current_results = state.get("research_results", [])
    updated_list = current_results + results
    new_index = idx + 1
    
    logger.info(f"run={state.get('run_id')} node=researcher status=finished subquestion={idx+1}/{len(plan)} found={len(results)}")
    
    return {
        "research_results": updated_list,
        "current_subquestion_index": new_index,
        "status": "researching"
    }

class Finding(BaseModel):
    claim: str
    supporting_source_urls: List[str]

class AnalysisResult(BaseModel):
    findings: List[Finding]
    needs_more_research: bool = Field(description="True only if there is a clear, specific gap to answer the plan.")
    reasoning: str

def analyzer_node(state: ResearchState) -> dict:
    """
    Analyzes gathered research to extract key findings and determines 
    if more research is needed to answer all sub-questions.
    """
    logger.info(f"run={state.get('run_id')} node=analyzer status=started")
    plan = state.get("plan", [])
    research_results = state.get("research_results", [])
    loop_count = state.get("research_loop_count", 0)
    
    llm = get_chat_model()
    structured_llm = llm.with_structured_output(AnalysisResult)
    
    prompt = (
        "You are an expert research analyst. Review the gathered research results and extract key findings to answer the original plan.\n"
        "Critically evaluate the findings: if two findings are near-duplicates of each other (same claim, different wording), flag this "
        "and treat it as a sign that the research needs to dig into a genuinely different angle rather than accepting redundant findings.\n\n"
        f"Plan:\n{json.dumps(plan, indent=2)}\n\n"
        f"Research Results:\n{json.dumps(research_results, indent=2)}\n\n"
        "Set needs_more_research=True ONLY if there is a clear, specific gap (not just 'could always know more') OR if the current findings are too repetitive/overlapping. "
        "State the gap in reasoning."
    )
    
    result = structured_llm.invoke(prompt)
    
    needs_more = result.needs_more_research
    if loop_count >= settings.max_research_loops:
        needs_more = False
        
    findings_list = [
        {"claim": f.claim, "supporting_sources": f.supporting_source_urls} 
        for f in result.findings
    ]
    
    state_update = {
        "findings": findings_list,
        "needs_more_research": needs_more,
        "status": "analyzing"
    }
    
    if needs_more:
        state_update["current_subquestion_index"] = 0
        state_update["research_loop_count"] = loop_count + 1
        
    logger.info(f"run={state.get('run_id')} node=analyzer status=finished needs_more={needs_more}")
    
    return state_update

def writer_node(state: ResearchState) -> dict:
    """
    Synthesizes a structured markdown report from the findings and 
    the original question.
    """
    logger.info(f"run={state.get('run_id')} node=writer status=started")
    question = state.get("original_question", "")
    findings = state.get("findings", [])
    
    llm = get_chat_model()
    
    prompt = (
        "You are an expert technical writer. Synthesize a structured markdown report based on the provided findings to answer the original question.\n"
        "Structure the report strictly by the sub-questions/facets. Each section MUST introduce information not covered elsewhere in the report. "
        "Explicitly DO NOT restate the same claim across multiple sections.\n"
        "Use numbered footnote markers like [1], [2] for inline citations after each claim drawn from a finding.\n"
        "Add a 'References' section at the end of the report listing each numbered source with its full URL.\n"
        "DO NOT fabricate sources — every citation in the report must correspond to a supporting_source_url that was actually in the findings.\n\n"
        f"Original Question: {question}\n\n"
        f"Findings:\n{json.dumps(findings, indent=2)}"
    )
    
    response = llm.invoke(prompt)
    report = response.content
    
    logger.info(f"run={state.get('run_id')} node=writer status=finished")
    
    return {
        "report": report,
        "status": "complete"
    }

