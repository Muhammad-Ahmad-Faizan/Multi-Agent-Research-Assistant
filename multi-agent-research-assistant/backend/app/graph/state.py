from typing import TypedDict, List, Dict, Optional

class ResearchState(TypedDict, total=False):
    original_question: str
    plan: List[str]
    plan_approved: bool
    current_subquestion_index: int
    research_results: List[Dict]
    findings: List[Dict]
    needs_more_research: bool
    research_loop_count: int
    report: str
    run_id: str
    status: str
    error_message: Optional[str]

def initial_state(question: str, run_id: str) -> ResearchState:
    return {
        "original_question": question,
        "run_id": run_id,
        "plan": [],
        "plan_approved": False,
        "current_subquestion_index": 0,
        "research_results": [],
        "findings": [],
        "needs_more_research": False,
        "research_loop_count": 0,
        "report": "",
        "status": "planning",
        "error_message": None
    }
