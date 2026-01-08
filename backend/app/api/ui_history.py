from fastapi import APIRouter
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter()
# Lưu tạm trong memory
HISTORY: List[Dict[str, Any]] = []

@router.get("/ui/history")
async def get_history():
    """Luôn trả về array"""
    try:
        print(f"🔍 [BACKEND] /ui/history called")
        
        # Đảm bảo HISTORY là list
        if not isinstance(HISTORY, list):
            print(f"⚠ HISTORY is not list, converting")
            return []
        
        # Sắp xếp
        sorted_history = sorted(
            HISTORY, 
            key=lambda x: x.get("date_checked", ""), 
            reverse=True
        )
        
        # Format response - đảm bảo là list
        response_data = []
        for item in sorted_history:
            if isinstance(item, dict):
                response_data.append({
                    "url": str(item.get("url", "")),
                    "compliance_score": float(item.get("compliance_score", 0)),
                    "level": str(item.get("level", "Non-compliant")),
                    "date_checked": str(item.get("date_checked", ""))
                })
        
        print(f"✅ [BACKEND] Returning {len(response_data)} items as list")
        
        # QUAN TRỌNG: Đảm bảo trả về list
        return response_data
        
    except Exception as e:
        print(f"❌ [BACKEND] Error: {e}")
        import traceback
        traceback.print_exc()
        return []  # Luôn trả về list rỗng

# Hàm helper để thêm vào history sau khi check
def add_history(url: str, score: float, level: str):
    try:
        HISTORY.append({
            "url": url,
            "compliance_score": float(score) if score is not None else 0.0,
            "level": str(level) if level else "Non-compliant",
            "date_checked": datetime.now().isoformat()
        })
        
        # Giới hạn history (giữ 50 items gần nhất)
        if len(HISTORY) > 50:
            HISTORY.pop(0)
            
    except Exception as e:
        print(f"❌ Error in add_history: {e}")