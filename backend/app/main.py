import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logger import logger
from backend.app.api.v1 import solver, chat, history, settings as sys_settings
from backend.app.models.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing SQLite database...")
    await init_db()
    logger.info("System startup complete. Ready to receive requests.")
    yield

app = FastAPI(
    title="AI Agent - Công nghệ Tự động hóa Lưới điện Phân phối",
    description="Hệ thống trợ lý học tập chuyên ngành: giải bài tập qua ảnh tiếng Trung và hỏi đáp chuyên ngành từ PDF giáo trình duy nhất.",
    version="1.2.0",
    lifespan=lifespan
)

# Cấu hình CORS cho cả Web (React Vite) và Desktop (Electron)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router REST API
app.include_router(solver.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(sys_settings.router, prefix="/api/v1")

@app.get("/api/health")
async def health_check():
    """Endpoint kiểm tra sức khỏe hệ thống (KPI-05, Phụ lục B)"""
    return {
        "status": "healthy",
        "service": "AI Distribution Grid Automation Agent",
        "version": "1.2.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
