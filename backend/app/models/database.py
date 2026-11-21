import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Float, Integer
from backend.app.core.config import settings

Base = declarative_base()

class DbSession(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_type: Mapped[str] = mapped_column(String(32), default="image_solver")
    title: Mapped[str] = mapped_column(String(255), default="Bài giải mới")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    data_json: Mapped[str] = mapped_column(Text, default="{}")

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
