import json
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from backend.app.agent.orchestrator import orchestrator
from backend.app.models.schemas import ChatMessageRequest, ChatResponse
from backend.app.models.database import get_session_by_id

router = APIRouter(prefix="/chat", tags=["Grounded Chat Q&A"])

@router.post("", response_model=ChatResponse)
async def chat_with_textbook(req: ChatMessageRequest):
    """
    Hỏi đáp chuyên ngành căn cứ vào nguồn PDF giáo trình tiếng Trung duy nhất (FR-12, FR-14, FR-23)
    Hỗ trợ duy trì ngữ cảnh hội thoại đa lượt (Multi-turn Context - FR-13)
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống")

    history = []
    # Nạp lịch sử các lượt trước nếu có session_id (FR-13)
    if req.session_id:
        existing = await get_session_by_id(req.session_id)
        if existing and existing.data_json:
            try:
                data = json.loads(existing.data_json)
                history = data.get("messages", [])
            except Exception:
                history = []

    result = await orchestrator.answer_chat(
        question=req.question,
        session_id=req.session_id,
        language=req.language,
        history=history
    )
    return result

@router.get("/{session_id}")
async def get_chat_session(session_id: str):
    """Lấy toàn bộ lịch sử các lượt trao đổi trong phiên chat (FR-13)"""
    session = await get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên hội thoại")
    try:
        return json.loads(session.data_json)
    except Exception:
        return {"session_id": session_id, "messages": []}
