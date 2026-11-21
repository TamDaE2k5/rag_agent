import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, select, delete
from backend.app.core.config import settings
from backend.app.core.logger import logger

Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class DbSession(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_type: Mapped[str] = mapped_column(String(32), default="image_solver")
    title: Mapped[str] = mapped_column(String(255), default="Bài giải mới")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    data_json: Mapped[str] = mapped_column(Text, default="{}")

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("SQLite database tables verified/created.")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def save_or_update_session(
    session_id: str,
    session_type: str,
    title: str,
    data: Dict[str, Any]
) -> DbSession:
    """Lưu hoặc cập nhật phiên làm việc vào SQLite (FR-15)"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(DbSession).where(DbSession.id == session_id)
            result = await session.execute(stmt)
            db_item = result.scalar_one_or_none()
            if db_item:
                db_item.title = title
                db_item.data_json = json.dumps(data, ensure_ascii=False)
                db_item.session_type = session_type
            else:
                db_item = DbSession(
                    id=session_id,
                    session_type=session_type,
                    title=title,
                    created_at=get_utc_now(),
                    data_json=json.dumps(data, ensure_ascii=False)
                )
                session.add(db_item)
        return db_item

async def get_session_by_id(session_id: str) -> Optional[DbSession]:
    """Truy vấn phiên theo ID"""
    async with AsyncSessionLocal() as session:
        stmt = select(DbSession).where(DbSession.id == session_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def list_recent_sessions(limit: int = 50) -> List[DbSession]:
    """Lấy danh sách các phiên gần đây sắp xếp giảm dần theo thời gian (FR-15)"""
    async with AsyncSessionLocal() as session:
        stmt = select(DbSession).order_by(DbSession.created_at.desc()).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())

async def delete_session_by_id(session_id: str) -> bool:
    """Xóa phiên khỏi database"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = delete(DbSession).where(DbSession.id == session_id)
            result = await session.execute(stmt)
            return result.rowcount > 0

async def clear_all_sessions() -> int:
    """Xóa toàn bộ lịch sử"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = delete(DbSession)
            result = await session.execute(stmt)
            return result.rowcount
