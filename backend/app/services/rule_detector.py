from app.services.sematic_detector import get_semantic_violations
from typing import Dict, List
from app.services.rules import COMPLIANCE_RULES
import re
from app.services.crawler import normalize_text


VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH"}

class RuleDetector:
    def __init__(self, text: str):
        self.text = (text or "").lower()
        self.semantic_results = get_semantic_violations(self.text)
        self.semantic_rule_ids = {r["rule_id"] for r in self.semantic_results}

        for rule in COMPLIANCE_RULES:
            if rule.get("severity", "LOW").upper() not in VALID_SEVERITIES:
                raise ValueError(f"Invalid severity {rule.get('severity')} in rule {rule.get('rule_id')}")

    def keyword_match(self, rule: Dict) -> bool:
        for kw in rule.get("keywords", []):
            pattern = rf"\b{re.escape(kw.lower())}\b"
            if re.search(pattern, self.text):
                return True
        return False

    def semantic_match_rule(self, rule: Dict) -> bool:
        return rule["rule_id"] in self.semantic_rule_ids

    def detect_rule(self, rule: Dict) -> bool:
        if self.keyword_match(rule):
            return True
        if rule.get("use_semantic", False):
            return self.semantic_match_rule(rule)
        return False

    def run(self) -> List[Dict]:
        results = []
        for rule in COMPLIANCE_RULES:
            passed = self.detect_rule(rule)
            results.append({
                "rule_id": rule.get("rule_id") or rule.get("id") or "unknown",
                "group": rule.get("group", "default"),
                "description": rule.get("description", ""),
                "passed": passed,
                "severity": rule.get("severity", "LOW").upper(),
                "weight": rule.get("weight", 1)
            })
        return results

    
    
