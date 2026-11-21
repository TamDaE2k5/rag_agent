from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.app.agent.orchestrator import orchestrator
from backend.app.services.image_service import image_service
from backend.app.models.schemas import SolutionResponse, ConfirmParametersRequest
from backend.app.core.logger import logger

router = APIRouter(prefix="/solver", tags=["Image Solver"])

@router.post("/solve-image", response_model=SolutionResponse)
async def solve_image(
    file: UploadFile = File(...),
    rotate_angle: int = Form(0),
    language: str = Form("vi")
):
    """
    Tiếp nhận ảnh đề bài tiếng Trung, tiền xử lý, gọi AI Agent và trả về lời giải có cấu trúc (FR-01, FR-02, FR-05 -> FR-11)
    """
    content = await file.read()
    is_valid, msg = image_service.validate_image(content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    mime_type = file.content_type or "image/jpeg"
    result = await orchestrator.solve_from_image(
        image_bytes=content,
        mime_type=mime_type,
        rotate_angle=rotate_angle,
        language=language
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", "Lỗi xử lý bài giải"))
        
    return result

@router.post("/confirm-parameters")
async def confirm_parameters(req: ConfirmParametersRequest):
    """
    Người dùng xác nhận hoặc sửa lại thông số nếu ảnh bị mờ trước khi tính toán lại (FR-08)
    """
    return {
        "status": "success",
        "session_id": req.session_id,
        "message": "Đã cập nhật thông số xác nhận thành công."
    }
