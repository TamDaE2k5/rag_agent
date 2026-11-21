import json
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import SessionItem
from backend.app.models.database import (
    list_recent_sessions,
    get_session_by_id,
    delete_session_by_id,
    clear_all_sessions,
    save_or_update_session
)
from backend.app.core.logger import logger

router = APIRouter(prefix="/history", tags=["History"])

# Dữ liệu hạt giống mặc định khi cơ sở dữ liệu trống
SEED_SESSIONS = [
    {
        "id": "demo-session-1",
        "type": "image_solver",
        "title": "Tính tổn thất điện áp đường dây 10kV",
        "data": {
            "final_answer": "P = 1200 kW, cos phi = 0.85, R = 2.5 Ohm -> Delta U = 538.08 V (5.38%)",
            "textbook_reference": "PDF giáo trình, trang 42"
        }
    },
    {
        "id": "demo-session-2",
        "type": "chat",
        "title": "Nguyên lý hoạt động của Dao cắt tự đóng lại (Recloser)",
        "data": {
            "latest_response": {
                "direct_answer": "Recloser tự động cắt và đóng lại theo chu trình cài đặt để phân biệt sự cố thoáng qua và vĩnh cửu."
            },
            "textbook_reference": "PDF giáo trình, trang 140"
        }
    }
]

def _extract_preview(session_type: str, data: Dict[str, Any]) -> str:
    """Tạo đoạn tóm tắt preview ngắn từ nội dung phiên"""
    if session_type == "image_solver":
        if "final_answer" in data:
            return str(data["final_answer"])[:120]
        params = data.get("extracted_data", {}).get("parameters", [])
        if params:
            param_strs = [f"{p.get('symbol')}={p.get('value')}" for p in params[:3] if p.get('value') is not None]
            return f"Thông số: {', '.join(param_strs)}"
        return "Bài giải bài tập phân phối điện qua ảnh"
    else:
        # Chat session
        latest = data.get("latest_response", {})
        if "direct_answer" in latest:
            return str(latest["direct_answer"])[:120]
        msgs = data.get("messages", [])
        if msgs:
            return str(msgs[-1].get("content", ""))[:120]
        return "Phiên hỏi đáp chuyên ngành RAG"

@router.get("", response_model=List[SessionItem])
async def get_history_list():
    """
    Lấy danh sách các phiên giải bài và hỏi đáp gần đây từ cơ sở dữ liệu SQLite (FR-15)
    """
    db_items = await list_recent_sessions(limit=50)

    # Nếu DB hoàn toàn trống (lần đầu khởi động), tạo sẵn seed demo
    if not db_items:
        for seed in SEED_SESSIONS:
            await save_or_update_session(
                session_id=seed["id"],
                session_type=seed["type"],
                title=seed["title"],
                data=seed["data"]
            )
        db_items = await list_recent_sessions(limit=50)

    result: List[SessionItem] = []
    for item in db_items:
        data = {}
        if item.data_json:
            try:
                data = json.loads(item.data_json)
            except Exception:
                data = {}

        created_str = (
            item.created_at.strftime("%Y-%m-%d %H:%M")
            if hasattr(item.created_at, "strftime")
            else str(item.created_at)[:16]
        )

        preview = _extract_preview(item.session_type, data)
        result.append(
            SessionItem(
                id=item.id,
                title=item.title or "Phiên làm việc",
                created_at=created_str,
                type=item.session_type,
                preview=preview
            )
        )
    return result

@router.get("/{session_id}")
async def get_session_detail(session_id: str):
    """Lấy chi tiết toàn bộ dữ liệu của một phiên đã lưu trong SQLite (FR-15)"""
    session = await get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên làm việc")

    try:
        data = json.loads(session.data_json)
    except Exception:
        data = {}

    return {
        "session_id": session.id,
        "session_type": session.session_type,
        "title": session.title,
        "created_at": str(session.created_at),
        "data": data
    }

@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Xóa một phiên làm việc khỏi lịch sử"""
    success = await delete_session_by_id(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên cần xóa")
    return {"status": "success", "message": f"Đã xóa phiên {session_id}"}

@router.delete("")
async def clear_history():
    """Xóa toàn bộ lịch sử các phiên"""
    count = await clear_all_sessions()
    return {"status": "success", "message": f"Đã xóa toàn bộ {count} phiên trong lịch sử."}
