from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AnalyzeRequest(BaseModel):
    url: Optional[str] = None
    policy_text: Optional[str] = None

class RuleResultSchema(BaseModel):
    rule_id: str
    group: str
    description: str
    passed: bool
    severity: str
    weight: Optional[float] = 1.0

class ComplianceReportSchema(BaseModel):
    compliance_score: float
    level: str
    summary: Dict[str, Any]
    rule_details: List[RuleResultSchema]  # Quan trọng: đổi từ violations -> rule_details
    high_risk: Optional[int] = 0