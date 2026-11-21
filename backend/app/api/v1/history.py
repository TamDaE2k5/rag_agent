from fastapi import APIRouter
from typing import List
from backend.app.models.schemas import SessionItem

router = APIRouter(prefix="/history", tags=["History"])

# In-memory / SQLite demo history
DEMO_SESSIONS: List[SessionItem] = [
    SessionItem(
        id="demo-session-1",
        title="Tính tổn thất điện áp đường dây 10kV",
        created_at="2026-11-21 16:30",
        type="image_solver",
        preview="P = 1200 kW, cos phi = 0.85, R = 2.5 Ohm -> Delta U = 538.08 V"
    ),
    SessionItem(
        id="demo-session-2",
        title="Nguyên lý hoạt động của Dao cắt tự đóng lại (Recloser)",
        created_at="2026-11-21 15:45",
        type="chat",
        preview="Cắt sự cố thoáng qua và tự động đóng lại theo chu trình cài đặt (Trang 140)"
    )
]

@router.get("", response_model=List[SessionItem])
async def get_history_list():
    """Lấy danh sách các phiên giải bài và hỏi đáp gần đây (FR-15)"""
    return DEMO_SESSIONS

@router.get("/{session_id}")
async def get_session_detail(session_id: str):
    return {
        "session_id": session_id,
        "detail": "Chi tiết phiên thao tác đã lưu."
    }
