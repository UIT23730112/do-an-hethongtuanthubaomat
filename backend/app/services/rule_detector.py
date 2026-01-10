from app.services.sematic_detector import get_semantic_violations
from typing import Dict, List
from app.services.rules import COMPLIANCE_RULES
import re
from app.services.crawler import normalize_text


VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH"}

class RuleDetector:
    def __init__(self, text: str):
        self.text = (text or "").lower()
        
        # Validate severities in rules
        for rule in COMPLIANCE_RULES:
            if rule.get("severity", "LOW").upper() not in VALID_SEVERITIES:
                raise ValueError(f"Invalid severity {rule.get('severity')} in rule {rule.get('rule_id')}")
        
        print(f"\n{'='*60}")
        print("🔍 RULE DETECTOR INITIALIZED")
        print(f"{'='*60}")
        print(f"📝 Text length: {len(self.text)} characters")
        
        # Phát hiện semantic violations
        print("\n🧠 Starting semantic analysis...")
        self.semantic_results = get_semantic_violations(self.text)
        
        # Tạo dict mapping rule_id -> violation details
        self.semantic_violations_dict = {}
        for v in self.semantic_results:
            self.semantic_violations_dict[v["rule_id"]] = {
                "severity": v.get("severity", "HIGH"),  # Mặc định HIGH nếu không có
                "similarity": v.get("similarity_score", 0),
                "description": v.get("description", "")
            }
        
        # Set của rule_ids có violation
        self.semantic_rule_ids = set(self.semantic_violations_dict.keys())
        
        if self.semantic_results:
            print(f"✅ Found {len(self.semantic_results)} semantic violations")
            for v in self.semantic_results[:3]:  # Show first 3
                lang = "VI" if v.get("language") == "vi" else "EN"
                print(f"   - {v['rule_id']} ({lang}): {v['similarity_score']:.3f}")
        else:
            print("ℹ️  No semantic violations detected")

    def keyword_match(self, rule: Dict) -> bool:
        """Keyword matching với regex"""
        keywords = rule.get("keywords", [])
        
        # Nếu keywords rỗng hoặc chỉ có dummy marker → không dùng keyword matching
        if not keywords or keywords == ["[SEMANTIC_ONLY]"]:
            return False
            
        for kw in keywords:
            pattern = rf"\b{re.escape(kw.lower())}\b"
            if re.search(pattern, self.text):
                return True
        return False

    def semantic_match_rule(self, rule: Dict) -> bool:
        """Kiểm tra xem rule này CÓ bị semantic violation không"""
        rule_id = rule.get("rule_id", "")
        has_violation = rule_id in self.semantic_rule_ids
        
        if has_violation:
            violation = self.semantic_violations_dict.get(rule_id, {})
            print(f"   🔍 Semantic VIOLATION: {rule_id}")
            print(f"      Severity: {violation.get('severity', 'HIGH')}")
            print(f"      Score: {violation.get('similarity', 0):.3f}")
        
        return has_violation

    def detect_rule(self, rule: Dict) -> bool:
        """
        Phát hiện rule với logic mới:
        
        SEMANTIC Rules:
        - CÓ vi phạm semantic → FAIL (passed=False) → ✗ LỖI (đỏ)
        - KHÔNG vi phạm semantic → PASS (passed=True) → ✓ ĐẠT (xanh)
        
        KEYWORD Rules:
        - Tìm thấy KEYWORD → PASS (passed=True) → ✓ ĐẠT (xanh)
        - KHÔNG tìm thấy keyword → FAIL (passed=False) → ✗ LỖI (đỏ)
        """
        rule_id = rule.get("rule_id", "")
        use_semantic = rule.get("use_semantic", False)
        keywords = rule.get("keywords", [])
        
        # Kiểm tra nếu là SEMANTIC-ONLY rule
        is_semantic_only = use_semantic and (not keywords or keywords == ["[SEMANTIC_ONLY]"])
        
        if is_semantic_only:
            # SEMANTIC-ONLY: CÓ vi phạm → FAIL, KHÔNG vi phạm → PASS
            has_violation = self.semantic_match_rule(rule)
            return not has_violation  # Đảo ngược logic: có vi phạm → False
        
        elif keywords and not use_semantic:
            # KEYWORD-ONLY: Tìm thấy keyword → PASS, Không tìm thấy → FAIL
            return self.keyword_match(rule)  # Giữ nguyên logic: tìm thấy → True
        
        elif keywords and use_semantic:
            # HYBRID: kết hợp cả hai
            keyword_found = self.keyword_match(rule)
            semantic_violation = self.semantic_match_rule(rule)
            
            # Logic: Nếu có keyword thì PASS (bất kể semantic)
            # Nếu không có keyword nhưng có semantic violation thì FAIL
            # Nếu không có cả hai thì xem xét theo config (tạm thời dùng keyword)
            if keyword_found:
                return True
            elif semantic_violation:
                return False
            else:
                return False  # Không có keyword, không có violation → FAIL
        
        else:
            # FALLBACK (không có config rõ ràng)
            print(f"⚠  [Warning] Rule {rule_id} has unclear detection method")
            return self.keyword_match(rule)

    def run(self) -> List[Dict]:
        """Chạy detection cho tất cả rules"""
        print(f"\n🎯 PROCESSING {len(COMPLIANCE_RULES)} RULES")
        print(f"{'='*60}")
        
        results = []
        semantic_rules_count = 0
        semantic_passed_count = 0
        
        for rule in COMPLIANCE_RULES:
            rule_id = rule.get("rule_id") or rule.get("id") or "unknown"
            is_semantic_rule = rule.get("use_semantic", False)
            
            if is_semantic_rule:
                semantic_rules_count += 1
            
            # Phát hiện rule
            passed = self.detect_rule(rule)
            
            # Xác định SEVERITY:
            # - Nếu là semantic rule và có violation → severity từ violation (luôn HIGH)
            # - Nếu là semantic rule và không violation → severity từ config (có thể HIGH/MEDIUM)
            # - Nếu là keyword rule → severity từ config
            if is_semantic_rule and not passed:  # Có semantic violation
                violation_data = self.semantic_violations_dict.get(rule_id, {})
                severity = violation_data.get("severity", "HIGH")  # Luôn HIGH
            else:
                severity = rule.get("severity", "LOW").upper()
            
            if is_semantic_rule:
                if passed:
                    semantic_passed_count += 1
                    print(f"✅ {rule_id}: SEMANTIC PASS (no violation)")
                else:
                    print(f"❌ {rule_id}: SEMANTIC FAIL (has violation)")
            
            results.append({
                "rule_id": rule_id,
                "group": rule.get("group", "default"),
                "description": rule.get("description", ""),
                "passed": passed,
                "severity": severity,  # ← SEVERITY ĐÚNG
                "weight": rule.get("weight", 1),
                "is_semantic": is_semantic_rule
            })
        
        # Thống kê
        print(f"\n{'='*60}")
        print("📊 FINAL RESULTS")
        print(f"{'='*60}")
        print(f"Total rules processed: {len(COMPLIANCE_RULES)}")
        print(f"Semantic rules: {semantic_passed_count}/{semantic_rules_count} passed")
        print(f"Total passed: {len([r for r in results if r['passed']])}")
        print(f"Total failed: {len([r for r in results if not r['passed']])}")
        
        return results