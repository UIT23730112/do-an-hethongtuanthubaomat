from typing import List, Dict, Any

def generate_compliance_report(rule_results: List[Dict], score_result: Dict) -> Dict[str, Any]:
    # Giữ nguyên tất cả rules
    all_rules = rule_results
    
    # Thống kê
    passed_count = len([r for r in rule_results if r.get("passed", False)])
    failed_count = len(rule_results) - passed_count
    
    # Thống kê severity của failed rules
    severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    high_risk_count = 0
    
    for r in rule_results:
        if not r.get("passed", False):
            sev = r.get("severity", "LOW").upper()
            if sev in severity_counts:
                severity_counts[sev] += 1
            if sev == "HIGH":
                high_risk_count += 1

    return {
        "compliance_score": score_result.get("score", 0.0),
        "level": score_result.get("level", "Non-compliant"),
        "summary": {
            "total_rules": len(rule_results),
            "passed_rules": passed_count,
            "failed_rules": failed_count,
            "high_risk": severity_counts["HIGH"],
            "medium_risk": severity_counts["MEDIUM"],
            "low_risk": severity_counts["LOW"]
        },
        "high_risk": high_risk_count,
        "rule_details": all_rules  # Gửi tất cả rules
    }