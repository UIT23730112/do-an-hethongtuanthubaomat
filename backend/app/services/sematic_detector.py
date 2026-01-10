from sentence_transformers import SentenceTransformer, util
import re
from typing import List, Dict

# ==================== MODEL LOADING ====================
model = None
try:
    print("🔄 Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Semantic model loaded successfully (multilingual - supports Vietnamese)")
    print(f"   Model info: {model.__class__.__name__}")
    print(f"   Max sequence length: {model.max_seq_length}")
except Exception as e:
    print(f"❌ Failed to load semantic model: {e}")
    print("⚠️  Semantic detection will be disabled")
    model = None

# ==================== BILINGUAL RULES ====================
SEMANTIC_RULES = [
    {
        "rule_id": "SEM-BI-01",
        "description_en": "Unlimited data collection",
        "description_vi": "Thu thập không giới hạn dữ liệu cá nhân",
        "patterns": [
            "We collect all available information about you",
            "We gather every piece of your personal data", 
            "Chúng tôi thu thập tất cả thông tin có sẵn về bạn",
            "Thu thập mọi dữ liệu cá nhân của bạn"
        ]
    },
    {
        "rule_id": "SEM-BI-02",
        "description_en": "Indefinite data storage",
        "description_vi": "Lưu trữ dữ liệu vô thời hạn",
        "patterns": [
            "Your data will be stored indefinitely without deletion",
            "Data retained permanently",
            "Dữ liệu sẽ được lưu trữ vĩnh viễn không xóa",
            "Lưu giữ thông tin mãi mãi"
        ]
    },
    {
        "rule_id": "SEM-BI-03",
        "description_en": "No security guarantee",
        "description_vi": "Từ chối trách nhiệm bảo mật dữ liệu",
        "patterns": [
            "We cannot guarantee the security of your information",
            "No security assurance for your data",
            "Không đảm bảo an toàn cho thông tin của bạn",
            "Không cam kết bảo mật dữ liệu"
        ]
    },
    {
        "rule_id": "SEM-BI-04",
        "description_en": "Forced waiver of complaint rights",
        "description_vi": "Ép buộc từ bỏ quyền khiếu nại",
        "patterns": [
            "You waive all rights to complain about data handling",
            "No right to complain about privacy practices",
            "Bạn từ bỏ quyền khiếu nại về cách xử lý dữ liệu",
            "Không được khiếu nại về bảo mật"
        ]
    },
    {
        "rule_id": "SEM-BI-05",
        "description_en": "Implied consent by continued use",
        "description_vi": "Đồng ý ngầm định",
        "patterns": [
            "Continued use means you agree to all terms",
            "Using the service constitutes acceptance",
            "Tiếp tục sử dụng có nghĩa là bạn đồng ý",
            "Truy cập website được xem như chấp nhận"
        ]
    },
    {
        "rule_id": "SEM-BI-06",
        "description_en": "Overly broad purpose specification",
        "description_vi": "Mục đích xử lý quá rộng",
        "patterns": [
            "We may use your data for any purpose we see fit",
            "Data used for various unspecified purposes",
            "Có thể dùng dữ liệu cho bất kỳ mục đích nào",
            "Sử dụng thông tin cho mọi mục tiêu"
        ]
    },
    {
        "rule_id": "SEM-BI-07",
        "description_en": "Disclaimed responsibility for data accuracy",
        "description_vi": "Từ chối trách nhiệm về tính chính xác",
        "patterns": [
            "We are not responsible for data accuracy",
            "No guarantee of information correctness",
            "Không chịu trách nhiệm về độ chính xác thông tin",
            "Không đảm bảo tính chính xác của dữ liệu"
        ]
    },
    {
        "rule_id": "SEM-BI-08",
        "description_en": "Overly broad data usage rights",
        "description_vi": "Trao quyền sử dụng dữ liệu quá rộng",
        "patterns": [
            "We have full rights to use your data as we wish",
            "Unlimited rights to utilize your information",
            "Chúng tôi có toàn quyền sử dụng dữ liệu của bạn",
            "Quyền sử dụng dữ liệu không hạn chế"
        ]
    }
]

# ==================== PRE-COMPUTE EMBEDDINGS ====================
rule_embeddings = {}
if model:
    print(f"📊 Computing embeddings for {len(SEMANTIC_RULES)} bilingual rules...")
    for rule in SEMANTIC_RULES:
        try:
            # Tính embedding cho tất cả patterns của rule này
            pattern_embeddings = []
            for pattern in rule["patterns"]:
                emb = model.encode(
                    pattern, 
                    convert_to_tensor=True,
                    show_progress_bar=False,
                    normalize_embeddings=True  # Normalize để cosine similarity chính xác
                )
                pattern_embeddings.append(emb)
            
            rule_embeddings[rule["rule_id"]] = {
                "embeddings": pattern_embeddings,
                "description_en": rule["description_en"],
                "description_vi": rule["description_vi"],
                "patterns": rule["patterns"]
            }
            
            print(f"   ✓ Encoded: {rule['rule_id']} ({len(pattern_embeddings)} patterns)")
            
        except Exception as e:
            print(f"⚠  Failed to encode rule {rule['rule_id']}: {e}")
    
    print(f"✅ Precomputed embeddings for {len(rule_embeddings)} rules")
    print(f"   Total pattern embeddings: {sum(len(data['embeddings']) for data in rule_embeddings.values())}")
else:
    print("⚠  Model not loaded, semantic detection disabled")

# ==================== LANGUAGE DETECTION ====================
def detect_language(text: str) -> str:
    """Phát hiện ngôn ngữ (vi/en) dựa trên ký tự tiếng Việt có dấu"""
    if not text or len(text.strip()) < 10:
        return 'en'
    
    text = text.lower()
    
    # Regex tìm ký tự tiếng Việt có dấu
    vietnamese_pattern = r'[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]'
    vietnamese_chars = re.findall(vietnamese_pattern, text)
    
    total_chars = len(text)
    
    # Nếu có >5% ký tự có dấu tiếng Việt → tiếng Việt
    if total_chars > 0 and len(vietnamese_chars) / total_chars > 0.05:
        return 'vi'
    
    return 'en'

# ==================== MAIN SEMANTIC DETECTION ====================
def get_semantic_violations(text: str, threshold: float = 0.65) -> List[Dict]:
    """
    Phát hiện vi phạm ngữ nghĩa - hỗ trợ song ngữ Anh-Việt
    
    Args:
        text: Văn bản cần phân tích
        threshold: Ngưỡng similarity (0.0-1.0)
    
    Returns:
        List các vi phạm phát hiện được
    """
    # Kiểm tra model
    if not model:
        print("❌ [Semantic] Model not loaded, semantic detection disabled")
        return []
    
    # Kiểm tra input
    if not text or len(text.strip()) < 20:
        print("⚠  [Semantic] Text too short for semantic analysis")
        return []
    
    print(f"\n{'='*60}")
    print("🧠 SEMANTIC ANALYSIS STARTED")
    print(f"{'='*60}")
    
    # Phát hiện ngôn ngữ
    language = detect_language(text)
    print(f"📝 Input text: {len(text)} characters")
    print(f"🌐 Detected language: {language.upper()}")
    
    # Điều chỉnh threshold theo ngôn ngữ
    # Tiếng Việt cần threshold thấp hơn vì model không tối ưu bằng tiếng Anh
    adjusted_threshold = threshold - 0.05 if language == 'vi' else threshold
    print(f"🎯 Using threshold: {adjusted_threshold:.2f} (base: {threshold:.2f})")
    
    violations = []
    
    try:
        # ========== STEP 1: Tạo embedding cho văn bản ==========
        print("🔧 Creating text embedding...")
        text_emb = model.encode(
            text,
            convert_to_tensor=True,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        
        # ========== STEP 2: So sánh với từng rule ==========
        print("🔍 Comparing with semantic rules...")
        
        for rule_id, rule_data in rule_embeddings.items():
            max_similarity = 0
            best_pattern_idx = -1
            
            # So sánh với tất cả patterns của rule này
            for i, pattern_emb in enumerate(rule_data["embeddings"]):
                similarity = util.cos_sim(text_emb, pattern_emb).item()
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_pattern_idx = i
            
            # Debug info cho mỗi rule
            if max_similarity > 0.4:  # Log nếu similarity > 0.4
                status = "✅ DETECTED" if max_similarity > adjusted_threshold else "ℹ️  below threshold"
                print(f"   {rule_id}: similarity={max_similarity:.3f} {status}")
            
            # Nếu similarity vượt ngưỡng → phát hiện vi phạm
            if max_similarity > adjusted_threshold:
                description = rule_data[f"description_{language}"]
                matched_pattern = rule_data["patterns"][best_pattern_idx] if best_pattern_idx >= 0 else ""
                
                violations.append({
                    "rule_id": rule_id,
                    "language": language,
                    "description": description,
                    "similarity_score": round(max_similarity, 3),
                    "matched_pattern": matched_pattern,
                    "threshold_used": adjusted_threshold,
                    "is_semantic": True,
                    "severity": "HIGH"  # ← THÊM DÒNG NÀY: Luôn là HIGH
                })
        
        # ========== STEP 3: Sắp xếp và log kết quả ==========
        violations.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        print(f"\n📊 RESULTS: {len(violations)} violations detected")
        if violations:
            for v in violations:
                print(f"   ✓ {v['rule_id']} ({v['language'].upper()}): {v['description'][:40]}...")
                print(f"      Similarity: {v['similarity_score']}, Pattern: {v['matched_pattern'][:50]}...")
        else:
            print("   No semantic violations found")
        
        print(f"{'='*60}")
        print("✅ SEMANTIC ANALYSIS COMPLETED")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Semantic detection error: {e}")
        import traceback
        traceback.print_exc()
    
    return violations

# ==================== ENHANCED DETECTION ====================
def get_privacy_violations_enhanced(text: str, semantic_threshold: float = 0.65) -> List[Dict]:
    """
    Phiên bản nâng cao: Kết hợp semantic và keyword matching
    
    Returns:
        List violations với cả semantic và keyword detections
    """
    violations = []
    
    # 1. Semantic detection
    semantic_violations = get_semantic_violations(text, semantic_threshold)
    violations.extend(semantic_violations)
    
    # 2. Keyword matching cho các cụm từ quan trọng
    keyword_red_flags = [
        # Tiếng Việt
        "không chịu trách nhiệm", "không đảm bảo", "vô thời hạn",
        "mãi mãi", "toàn quyền sử dụng", "từ bỏ quyền",
        # Tiếng Anh
        "not responsible", "no guarantee", "indefinitely",
        "forever", "full rights", "waive rights"
    ]
    
    text_lower = text.lower()
    
    for i, flag in enumerate(keyword_red_flags):
        if flag in text_lower:
            flag_lang = 'vi' if any(char in flag for char in 'àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ') else 'en'
            
            violations.append({
                "rule_id": f"KW-{flag_lang.upper()}-{i+1:02d}",
                "type": "keyword",
                "language": flag_lang,
                "description": f"Contains phrase: '{flag}'",
                "similarity_score": 1.0,
                "matched_pattern": flag,
                "is_semantic": False
            })
    
    return violations