from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="Hệ thống kiểm tra mức độ chính sách bảo mật",
    description="Automatic GDPR & Vietnam PDPL (Decree 91/2025) compliance checker",
    version="0.1.0"
)

# Thêm các origins
# Tìm origins và thêm:
origins = [
    "http://localhost:3000",
    "http://localhost:8000", 
    "https://uit23730112.github.io",
    "https://uit23730112.github.io/do-an-hethongtuanthubaomat",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # Thêm dòng này
)

# Routes
from .api import analyze, ui_history, ui

# Chỉ include các API endpoints
app.include_router(analyze.router, prefix="/api", tags=["analysis"])
app.include_router(ui_history.router, prefix="/api", tags=["history"])
app.include_router(ui.router, prefix="/api", tags=["ui"])

# Xóa endpoint /analyze trùng lặp trong main.py
# Xóa endpoint POST /analyze trong main.py (đã có trong analyze.py)

# Serve React app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REACT_BUILD_DIR = os.path.join(BASE_DIR, "frontend-react", "build")

@app.get("/{full_path:path}")
def serve_react(full_path: str):
    index_path = os.path.join(REACT_BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "React app not built. Run 'npm run build' in frontend-react directory."}

# Health check
@app.get("/health")
def health_check():
    return {"status": "totally fine"}

@app.get("/debug/routes")
def debug_routes():
    routes = []
    for route in app.routes:
        route_info = {
            "path": route.path,
            "name": getattr(route, "name", "N/A"),
        }
        if hasattr(route, "methods"):
            route_info["methods"] = list(route.methods)
        routes.append(route_info)
    return routes
# Thêm vào main.py
@app.get("/api/debug/history")
def debug_history():
    """Debug endpoint - luôn trả về array"""
    return [
        {
            "url": "https://example.com",
            "compliance_score": 85.5,
            "level": "Compliant",
            "date_checked": "2024-01-01T12:00:00"
        },
        {
            "url": "https://test.com", 
            "compliance_score": 30.2,
            "level": "Non-compliant",
            "date_checked": "2024-01-02T12:00:00"
        }
    ]
# Test endpoint đơn giản
@app.post("/api/test")
def test_endpoint():
    return {"message": "Test endpoint works!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)