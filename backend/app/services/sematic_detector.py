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
    # Các rule cũ về tài chính (giữ nguyên)
    {"rule_id": "R01", "description": "Claims guaranteed profit"},
    {"rule_id": "R02", "description": "No risk investment"},
    
    # Thêm một số rule SEMANTIC QUAN TRỌNG về bảo vệ dữ liệu
    # (Chọn những rule có thể phát hiện bằng semantic thay vì keyword matching)
    {
        "rule_id": "PRIV-01", 
        "description": "We collect all your personal data without limitation"
    },
    {
        "rule_id": "PRIV-02", 
        "description": "We can share your data with anyone without your consent"
    },
    {
        "rule_id": "PRIV-03", 
        "description": "We keep your data forever without deletion"
    },
    {
        "rule_id": "PRIV-04", 
        "description": "You cannot access or modify your personal information"
    },
    {
        "rule_id": "PRIV-05", 
        "description": "We are not responsible for data breaches or leaks"
    },
    {
        "rule_id": "PRIV-06", 
        "description": "We own all your data and can use it for any purpose"
    }
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