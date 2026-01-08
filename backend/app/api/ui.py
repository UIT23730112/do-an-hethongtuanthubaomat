from fastapi import APIRouter, HTTPException
from app.services.rule_detector import RuleDetector
from app.services.scoring import calculate_compliance_score
from app.services.report import generate_compliance_report
from app.services.crawler import crawl_and_normalize, normalize_text
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UIAnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

@router.post("/ui/analyze")
def analyze_ui(payload: UIAnalyzeRequest):
    """
    API endpoint tương tự /api/analyze nhưng với tham số khác
    (giữ cho tương thích nếu frontend cũ đang dùng)
    """
    if not payload.text and not payload.url:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp URL hoặc văn bản")

    policy_text = ""

    if payload.url:
        policy_text = crawl_and_normalize(payload.url)
    elif payload.text: 
        policy_text = normalize_text(payload.text)

    detector = RuleDetector(policy_text)
    rules = detector.run()
    score_result = calculate_compliance_score(rules)
    report = generate_compliance_report(rules, score_result)

    return report