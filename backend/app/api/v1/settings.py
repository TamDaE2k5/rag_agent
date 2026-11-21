import os
from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.core.config import settings

router = APIRouter(prefix="/settings", tags=["Settings"])

class SettingsResponse(BaseModel):
    model_name: str
    default_language: str
    textbook_pdf_exists: bool
    total_indexed_pages: int
    has_api_key: bool

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
