from fastapi import APIRouter, HTTPException
from app.services.rule_detector import RuleDetector
from app.services.scoring import calculate_compliance_score
from app.services.report import generate_compliance_report
from app.services.crawler import crawl_policy, normalize_text
from app.api.ui_history import add_history
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: Optional[str] = None
    policy_text: Optional[str] = None

class RuleResultSchema(BaseModel):
    rule_id: str
    group: str
    description: str
    passed: bool
    severity: str
    weight: Optional[float] = None

class AnalyzeResponse(BaseModel):
    compliance_score: float
    level: str
    rule_details: list[RuleResultSchema]  # Đổi từ results -> rule_details
    summary: dict
    high_risk: Optional[int] = 0

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_policy(payload: AnalyzeRequest):
    # 1. Lấy text từ URL hoặc text trực tiếp
    policy_text = ""
    
    if payload.url:
        raw_text = crawl_policy(payload.url)
        policy_text = normalize_text(raw_text)
    elif payload.policy_text:
        policy_text = normalize_text(payload.policy_text)
    else:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp URL hoặc văn bản chính sách")

    # 2. Rule detection
    detector = RuleDetector(policy_text)
    rule_results = detector.run()

    # 3. Tính điểm và tạo report
    score_result = calculate_compliance_score(rule_results)
    report = generate_compliance_report(rule_results, score_result)
    
    # 4. Lưu vào history nếu có URL
    if payload.url:
        add_history(payload.url, report["compliance_score"], report["level"])

    # 5. Map rule results cho response
    rule_details = [
        RuleResultSchema(
            rule_id=r.get("rule_id", ""),
            group=r.get("group", ""),
            description=r.get("description", ""),
            passed=r.get("passed", False),
            severity=r.get("severity", "LOW"),
            weight=r.get("weight", 1.0)
        )
        for r in rule_results
    ]

    return AnalyzeResponse(
        compliance_score=report["compliance_score"],
        level=report["level"],
        rule_details=rule_details,  # Đúng tên field frontend mong đợi
        summary=report["summary"],
        high_risk=report.get("high_risk", 0)
    )