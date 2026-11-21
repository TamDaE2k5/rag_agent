import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file manually if exists
env_path = BASE_DIR / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "vi")
        
        self.TEXTBOOK_PDF_PATH: str = os.getenv(
            "TEXTBOOK_PDF_PATH", str(BASE_DIR / "knowledge" / "course_textbook.pdf")
        )
        self.INDEX_DIR: str = str(BASE_DIR / "knowledge" / "index")
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/agent_app.db"
        )
        
        self.HOST: str = os.getenv("HOST", "127.0.0.1")
        self.PORT: int = int(os.getenv("PORT", "8000"))
        self.DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")
        self.CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
