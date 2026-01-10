# sematic_detector.py
from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✓ Semantic model loaded successfully")
except Exception as e:
    print(f"✗ Failed to load semantic model: {e}")
    model = None


SEMANTIC_RULES = [
    # Map với rules.py
    {"rule_id": "SEM-LFT-01", "description": "We may use your data as we see fit for business purposes"},
    {"rule_id": "SEM-PL-01", "description": "Your data may be used for various purposes including improvement of services"},
    {"rule_id": "SEM-DM-01", "description": "We collect all available information about you from various sources"},
    {"rule_id": "SEM-AC-01", "description": "We are not responsible for the accuracy of personal information provided by users"},
    {"rule_id": "SEM-SL-01", "description": "Your personal data will be retained indefinitely for future reference"},
    {"rule_id": "SEM-IC-01", "description": "We cannot guarantee the security of your data during transmission over the internet"},
    {"rule_id": "SEM-ACT-01", "description": "By using this service, you waive all rights to complain about data handling practices"},
    {"rule_id": "SEM-CONSENT-01", "description": "Continued use of this website constitutes your agreement to all terms without explicit consent"}
]
# Tạo embeddings cho tất cả rule
rule_embeddings = {}
if model:
    for r in SEMANTIC_RULES:
        try:
            rule_embeddings[r["rule_id"]] = model.encode(
                r["description"], 
                convert_to_tensor=True,
                show_progress_bar=False
            )
        except Exception as e:
            print(f"✗ Failed to encode rule {r['rule_id']}: {e}")

def get_semantic_violations(text: str, threshold: float = 0.65):
    """
    Phát hiện vi phạm ngữ nghĩa trong văn bản
    """
    if not model or not text:
        return []
    
    violations = []
    
    try:
        # Chuyển văn bản thành embedding
        text_emb = model.encode(text, convert_to_tensor=True, show_progress_bar=False)
        
        # So sánh với từng rule
        for rule in SEMANTIC_RULES:
            if rule["rule_id"] not in rule_embeddings:
                continue
                
            similarity = util.cos_sim(text_emb, rule_embeddings[rule["rule_id"]]).item()
            
            if similarity > threshold:
                violations.append({
                    "rule_id": rule["rule_id"],
                    "type": "semantic",
                    "description": rule["description"],
                    "score": round(similarity, 2),
                    "matched_text_snippet": text[:100] + "..." if len(text) > 100 else text
                })
    except Exception as e:
        print(f"✗ Semantic detection error: {e}")
    
    return violations



def get_privacy_violations_enhanced(text: str, semantic_threshold: float = 0.7):
    """
    Phiên bản nâng cao: Kết hợp semantic và keyword matching
    """
    violations = []
    
    # 1. Kiểm tra semantic violations
    semantic_violations = get_semantic_violations(text, semantic_threshold)
    violations.extend(semantic_violations)
    
    # 2. Có thể thêm keyword checking ở đây nếu cần
    privacy_red_flags = [
        "without your consent",
        "cannot delete",
        "forever",
        "unlimited use",
        "no responsibility",
        "own your data",
        "share with third parties without notice"
    ]
    
    keyword_violations = []
    for i, flag in enumerate(privacy_red_flags):
        if flag.lower() in text.lower():
            keyword_violations.append({
                "rule_id": f"KW-PRIV-{i+1:02d}",
                "type": "keyword",
                "description": f"Contains phrase: '{flag}'",
                "score": 1.0,
                "matched_text": flag
            })
    
    violations.extend(keyword_violations)
    
    return violations


# Ví dụ sử dụng
if __name__ == "__main__":
    test_text = """
    By using our service, you agree that we can collect all your personal data 
    and share it with any third-party partners without your explicit consent. 
    We reserve the right to keep your data indefinitely and use it for any 
    commercial purposes we see fit. You cannot request deletion of your data.
    """
    
    print("=== SEMANTIC VIOLATIONS ===")
    violations = get_semantic_violations(test_text, threshold=0.65)
    for v in violations:
        print(f"Rule {v['rule_id']}: {v['description']}")
        print(f"  Score: {v['score']}")
        print(f"  Snippet: {v['matched_text_snippet']}")
        print()
    
    print("\n=== ENHANCED DETECTION ===")
    enhanced = get_privacy_violations_enhanced(test_text)
    for v in enhanced:
        print(f"[{v['type'].upper()}] {v['rule_id']}: {v.get('description', 'N/A')}")

        from app.services.sematic_detector import detect_semantic_violations_bilingual
