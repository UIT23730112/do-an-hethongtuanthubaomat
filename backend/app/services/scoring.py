from typing import List, Dict

COMPLIANCE_LEVELS = [
    {"min": 80, "label": "Compliant"},
    {"min": 50, "label": "Upper partially compliant"},
    {"min": 25, "label": "Lower partially compliant"},
    {"min": 0,  "label": "Non-compliant"},
]

def calculate_compliance_score(rules: List[Dict]) -> Dict:
    if not rules:
        return {
            "score": 0.0,
            "level": "Non-compliant",
            "summary": {
                "passed_rules": 0,
                "failed_rules": 0,
                "high_risk": 0,
                "medium_risk": 0,
                "low_risk": 0,
            }
        }
    
    total_weight = 0
    achieved_weight = 0
    
    # Đếm risk levels
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

    passed_count = 0
    failed_count = 0

    for rule in rules:
        weight = rule.get("weight", 1)
        
        if rule.get("is_semantic", False):
            # SEMANTIC RULES: chỉ tính khi FAIL (trừ điểm)
            if rule.get("passed", False):
                # PASS: không có violation → không cộng, không trừ
                passed_count += 1
                # KHÔNG thêm vào total_weight và achieved_weight
            else:
                # FAIL: có violation → TRỪ ĐIỂM
                failed_count += 1
                severity = "HIGH"  # Semantic violations luôn HIGH
                high_risk_count += 1
                
                # Tính điểm: thêm weight vào total, TRỪ khỏi achieved
                total_weight += weight
                achieved_weight -= weight  # Hoặc weight * 2 nếu muốn phạt nặng
                
        else:
            # KEYWORD RULES: logic cũ (bình thường)
            total_weight += weight

            if rule.get("passed", False):
                achieved_weight += weight
                passed_count += 1
            else:
                failed_count += 1
                severity = rule.get("severity", "LOW").upper()
                
                if severity == "HIGH":
                    high_risk_count += 1
                elif severity == "MEDIUM":
                    medium_risk_count += 1
                elif severity == "LOW":
                    low_risk_count += 1

    # Tính điểm - QUAN TRỌNG: cần xử lý đặc biệt
    if total_weight == 0:
        score = 0.0
    else:
        # Tính phần trăm đạt được
        raw_score = (achieved_weight / total_weight) * 100
        
        # Đảm bảo điểm không âm
        score = max(0.0, raw_score)
    
    # Xác định compliance level
    compliance_level = "Non-compliant"
    for level in COMPLIANCE_LEVELS:
        if score >= level["min"]:
            compliance_level = level["label"]
            break

    return {
        "score": round(score, 2),
        "level": compliance_level,
        "summary": {
            "passed_rules": passed_count,
            "failed_rules": failed_count,
            "high_risk": high_risk_count,
            "medium_risk": medium_risk_count,
            "low_risk": low_risk_count,
        }
    }