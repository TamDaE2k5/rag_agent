import os
import json
import re
import math
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from backend.app.core.config import settings
from backend.app.core.logger import logger
from backend.app.services.vector_store import vector_store

VI_TO_ZH_TERMS = {
    "sơ đồ nối dây": "接线",
    "nối dây": "接线",
    "thiết bị nhất thứ": "一次设备",
    "nhất thứ": "一次设备",
    "thiết bị nhị thứ": "二次设备",
    "nhị thứ": "二次设备",
    "lưới điện phân phối": "配电网",
    "lưới phân phối": "配电网",
    "tự động hóa": "自动化",
    "thông minh": "智能化",
    "trí tuệ": "智能化",
    "chức năng": "功能",
    "tổn thất điện áp": "电压降",
    "sụt áp": "电压降",
    "ngắn mạch": "短路",
    "bù công suất": "无功补偿",
    "dao cắt tự đóng lại": "重合器",
    "recloser": "重合器",
    "dao phân đoạn": "分段器",
    "sectionalizer": "分段器",
    "truyền thông": "通信",
    "chẵn lẻ": "奇偶校验",
    "chẵn lẻ ngang dọc": "水平垂直一致校验",
    "phân đoạn": "分段",
    "sự cố": "故障",
    "cô lập sự cố": "故障隔离"
}

class RAGService:
    """
    Dịch vụ RAG kết hợp (Hybrid Search: Vector Search + Keyword Search)
    Nguồn tri thức duy nhất: PDF giáo trình tiếng Trung (FR-14, FR-23)
    Hỗ trợ cầu nối ngôn ngữ Việt - Trung (Bilingual terminology expansion)
    """
    def __init__(self):
        self.index_file = os.path.join(settings.INDEX_DIR, "pages.json")
        self.vocab_file = os.path.join(settings.INDEX_DIR, "vocab.json")
        self.pages: List[Dict[str, Any]] = []
        self.vocab: List[str] = []
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

        if os.path.exists(self.vocab_file):
            try:
                with open(self.vocab_file, "r", encoding="utf-8") as f:
                    self.vocab = json.load(f)
                logger.info(f"Loaded {len(self.vocab)} bigram vocabulary terms for vector search.")
            except Exception as e:
                logger.error(f"Error loading vocab file: {e}")
                self.vocab = []
        elif self.pages:
            from collections import Counter
            corpus = [p["text"] for p in self.pages]
            vocab_counter = Counter()
            for doc in corpus:
                for i in range(len(doc) - 1):
                    bg = doc[i:i+2]
                    if '\u4e00' <= bg[0] <= '\u9fff' and '\u4e00' <= bg[1] <= '\u9fff':
                        vocab_counter[bg] += 1
            self.vocab = [term for term, count in vocab_counter.most_common(256)]
            try:
                with open(self.vocab_file, "w", encoding="utf-8") as f:
                    json.dump(self.vocab, f, ensure_ascii=False)
            except Exception as ex:
                logger.warning(f"Could not persist vocab file: {ex}")

    def expand_query(self, query: str) -> str:
        """Mở rộng từ khóa chuyên ngành Việt - Trung để tra cứu chính xác"""
        q_lower = query.lower()
        extra_terms = []
        for vi, zh in VI_TO_ZH_TERMS.items():
            if vi in q_lower:
                extra_terms.append(zh)
        if extra_terms:
            return query + " " + " ".join(extra_terms)
        return query

    def vectorize_query(self, query: str) -> np.ndarray:
        """
        Chuyển đổi câu truy vấn thành vector đặc trưng trong không gian 256 chiều
        của ma trận vectors.npy (Bigram TF-IDF / Log-frequency).
        """
        if not self.vocab:
            return np.zeros(256, dtype=np.float32)
        
        expanded = self.expand_query(query)
        v = np.zeros(len(self.vocab), dtype=np.float32)
        for i, term in enumerate(self.vocab):
            count = expanded.count(term)
            if count > 0:
                v[i] = 1.0 + math.log(count)
        norm = np.linalg.norm(v)
        if norm > 0:
            v = v / norm
        return v

    def embed_text_with_google(self, text: str) -> Optional[List[float]]:
        if not settings.GEMINI_API_KEY:
            return None
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.embed_content(
                model="models/text-embedding-004",
                contents=text
            )
            if hasattr(response, "embedding") and hasattr(response.embedding, "values"):
                return response.embedding.values
            elif hasattr(response, "embeddings") and len(response.embeddings) > 0:
                return response.embeddings[0].values
        except Exception as e:
            logger.debug(f"Google embedding API call skipped/failed: {e}")
            return None

    def search_vector(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Tìm kiếm ngữ nghĩa bằng Cosine Similarity trên ma trận vectors.npy (233 trang) (FR-23)
        """
        if vector_store.embeddings is None or len(vector_store.metadata) == 0:
            return []

        q_vec = self.vectorize_query(query)
        if np.linalg.norm(q_vec) > 0:
            return vector_store.search_by_vector(q_vec.tolist(), top_k=top_k)
        return []

    def search_keyword(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Tìm kiếm theo từ khóa / tần suất xuất hiện (Sparse Retrieval)"""
        if not self.pages:
            self._load_index()
            if not self.pages:
                return []

        expanded = self.expand_query(query)
        keywords = [k.strip() for k in re.split(r"[\s,;，、]+", expanded) if len(k.strip()) >= 2]
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
                    "score": float(score),
                    "text": text[:1200],
                    "reference": f"PDF giáo trình, trang {p['page_number']}"
                })

        scored_pages.sort(key=lambda x: x["score"], reverse=True)
        return scored_pages[:top_k]

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Tìm kiếm Hybrid RAG (FR-23):
        1. Thực hiện Vector Search bằng Cosine Similarity trên vectors.npy (233 trang).
        2. Thực hiện Keyword Search (Sparse Retrieval) dựa trên tần suất xuất hiện từ khóa.
        3. Kết hợp và xếp hạng lại.
        """
        vector_results = []
        if vector_store.embeddings is not None and len(vector_store.metadata) > 0:
            try:
                vector_results = self.search_vector(query, top_k=top_k * 2)
            except Exception as e:
                logger.warning(f"Vector search failed, falling back to keyword search: {e}")

        keyword_results = self.search_keyword(query, top_k=top_k * 2)

        if not vector_results and not keyword_results:
            return []
        if not vector_results:
            return keyword_results[:top_k]
        if not keyword_results:
            return vector_results[:top_k]

        max_kw_score = max((r.get("score", 1.0) for r in keyword_results), default=1.0)
        if max_kw_score <= 0:
            max_kw_score = 1.0

        page_dict: Dict[int, Dict[str, Any]] = {}

        for r in vector_results:
            p_num = r["page_number"]
            sim = r.get("similarity_score", 0.0)
            page_dict[p_num] = {
                "page_number": p_num,
                "score": float(sim * 0.6),
                "text": r["text"],
                "reference": r["reference"],
                "vector_sim": sim,
                "keyword_score": 0.0
            }

        for r in keyword_results:
            p_num = r["page_number"]
            norm_kw = (r.get("score", 0.0) / max_kw_score) * 0.4
            if p_num in page_dict:
                page_dict[p_num]["score"] += norm_kw
                page_dict[p_num]["keyword_score"] = r.get("score", 0.0)
            else:
                page_dict[p_num] = {
                    "page_number": p_num,
                    "score": float(norm_kw),
                    "text": r["text"],
                    "reference": r["reference"],
                    "vector_sim": 0.0,
                    "keyword_score": r.get("score", 0.0)
                }

        combined_results = sorted(page_dict.values(), key=lambda x: x["score"], reverse=True)
        return combined_results[:top_k]

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
