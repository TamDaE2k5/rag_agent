import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.app.core.config import settings
from backend.app.providers.gemini_provider import gemini_provider

router = APIRouter(prefix="/settings", tags=["Settings"])

class SettingsResponse(BaseModel):
    model_name: str
    default_language: str
    textbook_pdf_exists: bool
    total_indexed_pages: int
    has_api_key: bool

class ConnectionTestResponse(BaseModel):
    connected: bool
    status: str
    model: str
    message: str
    mode: str

@router.get("", response_model=SettingsResponse)
async def get_settings():
    """Lấy thông tin cấu hình hệ thống (FR-20)"""
    from backend.app.services.rag_service import rag_service
    has_key = bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 10)
    pdf_exists = os.path.exists(settings.TEXTBOOK_PDF_PATH)
    
    return SettingsResponse(
        model_name=settings.GEMINI_MODEL,
        default_language=settings.DEFAULT_LANGUAGE,
        textbook_pdf_exists=pdf_exists,
        total_indexed_pages=len(rag_service.pages),
        has_api_key=has_key
    )

@router.get("/test-connection", response_model=ConnectionTestResponse)
@router.post("/test-connection", response_model=ConnectionTestResponse)
async def test_gemini_connection():
    """
    Kiểm tra trạng thái kết nối tới Google Gemini REST API và chế độ hoạt động (Online / Local RAG)
    """
    result = gemini_provider.test_connection()
    return ConnectionTestResponse(
        connected=result.get("connected", False),
        status=result.get("status", "offline_local_rag"),
        model=result.get("model", settings.GEMINI_MODEL),
        message=result.get("message", "Đang hoạt động ở chế độ Local RAG."),
        mode=result.get("mode", "local_rag")
    )
