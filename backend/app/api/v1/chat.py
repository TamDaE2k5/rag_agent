from fastapi import APIRouter, HTTPException
from backend.app.agent.orchestrator import orchestrator
from backend.app.models.schemas import ChatMessageRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Grounded Chat Q&A"])

@router.post("", response_model=ChatResponse)
async def chat_with_textbook(req: ChatMessageRequest):
    """
    Hỏi đáp chuyên ngành căn cứ vào nguồn PDF giáo trình tiếng Trung duy nhất (FR-12, FR-14, FR-23)
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống")
        
    result = await orchestrator.answer_chat(
        question=req.question,
        session_id=req.session_id,
        language=req.language
    )
    return result
