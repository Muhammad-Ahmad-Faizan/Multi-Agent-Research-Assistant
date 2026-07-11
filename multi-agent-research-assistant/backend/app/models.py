from pydantic import BaseModel
from typing import List, Optional

class RunStatusResponse(BaseModel):
    run_id: str
    status: str
    plan: List[str]
    current_subquestion_index: int
    findings_count: int
    report: Optional[str] = None
    error_message: Optional[str] = None
