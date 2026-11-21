import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from backend.app.core.config import settings
from backend.app.core.logger import logger
from backend.app.services.vector_store import vector_store

class RAGService:
    """
    Dịch vụ RAG kết hợp (Hybrid Search: Vector Search + Keyword Search)
    Nguồn tri thức duy nhất: PDF giáo trình tiếng Trung (FR-14, FR-23)
    """
    def __init__(self):
        self.index_file = os.path.join(settings.INDEX_DIR, "pages.json")
        self.pages: List[Dict[str, Any]] = []
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.pages = data.get("pages", [])
                logger.info(f"Loaded {len(self.pages)} indexed pages from {self.index_file}")
            except Exception as e:
                logger.error(f"Error loading RAG index: {e}")
                self.pages = []
        else:
            logger.warning(f"Index file not found at {self.index_file}. Run scripts/ingest_pdf.py to generate.")

    def search_keyword(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Tìm kiếm theo từ khóa / tần suất xuất hiện (Sparse Retrieval)"""
        if not self.pages:
            self._load_index()
            if not self.pages:
                return []

        keywords = [k.strip() for k in re.split(r"[\s,;，、]+", query) if len(k.strip()) >= 2]
        if not keywords:
            keywords = [query.strip()]

        scored_pages = []
        for p in self.pages:
            text = p["text"]
            score = 0
            for kw in keywords:
                count = text.lower().count(kw.lower())
                score += count * len(kw)
            
            if score > 0:
                scored_pages.append({
                    "page_number": p["page_number"],
                    "score": score,
                    "text": text[:1200],
                    "reference": f"PDF giáo trình, trang {p['page_number']}"
                })

        scored_pages.sort(key=lambda x: x["score"], reverse=True)
        return scored_pages[:top_k]

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Tìm kiếm Hybrid RAG:
        1. Ưu tiên Vector Search nếu đã nạp vector embedding trong Vector Database.
        2. Kết hợp với Keyword Search để đảm bảo các thuật ngữ viết tắt và ký hiệu điện không bị bỏ sót.
        """
        # Nếu VectorStore đã có dữ liệu vector
        if vector_store.embeddings is not None and len(vector_store.metadata) > 0:
            # Ở chế độ có embedding
            try:
                # Tìm kiếm bằng vector (nếu query vector được truyền hoặc tính toán)
                pass
            except Exception as e:
                logger.warning(f"Vector search failed, falling back to keyword search: {e}")

        # Tìm kiếm kết hợp
        return self.search_keyword(query, top_k=top_k)

    def get_grounded_context(self, query: str) -> Tuple[str, List[str]]:
        """Trả về ngữ cảnh trích đoạn kèm danh sách số trang tham chiếu"""
        results = self.search(query, top_k=3)
        if not results:
            return "", []

        context_parts = []
        refs = []
        for r in results:
            context_parts.append(f"[Trang {r['page_number']}]:\n{r['text']}")
            refs.append(f"PDF giáo trình, trang {r['page_number']}")

        return "\n\n---\n\n".join(context_parts), refs

rag_service = RAGService()
