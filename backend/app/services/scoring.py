from typing import List, Dict

COMPLIANCE_LEVELS = [
    {"min": 85, "label": "Compliant"},
    {"min": 70, "label": "Upper partially compliant"},
    {"min": 50, "label": "Lower partially compliant"},
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
    
    severity_count = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    passed_count = 0
    failed_count = 0

    for rule in rules:
        weight = rule.get("weight", 1)
        total_weight += weight

        if rule.get("passed", False):
            achieved_weight += weight
            passed_count += 1
        else:
            failed_count += 1
            severity = rule.get("severity", "LOW").upper()
            if severity not in severity_count:
                severity = "LOW"
            severity_count[severity] += 1

    # Xử lý chia cho 0
    if total_weight == 0:
        score = 0.0
    else:
        score = round((achieved_weight / total_weight) * 100, 2)

    compliance_level = "Non-compliant"
    for level in COMPLIANCE_LEVELS:
        if score >= level["min"]:
            compliance_level = level["label"]
            break

    return {
        "score": score,
        "level": compliance_level,
        "summary": {
            "passed_rules": passed_count,
            "failed_rules": failed_count,
            "high_risk": severity_count["HIGH"],
            "medium_risk": severity_count["MEDIUM"],
            "low_risk": severity_count["LOW"],
        }
    }