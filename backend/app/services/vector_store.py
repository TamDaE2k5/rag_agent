import os
import json
import math
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from backend.app.core.config import settings
from backend.app.core.logger import logger

class VectorStore:
    """
    Hệ thống lưu trữ và tìm kiếm Vector (Vector Database) chuẩn cho RAG
    Hỗ trợ tính toán độ tương đồng Cosine Similarity trên không gian vector embedding.
    """
    def __init__(self):
        self.vectors_file = os.path.join(settings.INDEX_DIR, "vectors.npy")
        self.metadata_file = os.path.join(settings.INDEX_DIR, "vector_metadata.json")
        self.embeddings: Optional[np.ndarray] = None
        self.metadata: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.vectors_file) and os.path.exists(self.metadata_file):
            try:
                self.embeddings = np.load(self.vectors_file)
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded Vector Database with {len(self.metadata)} vectors (dim: {self.embeddings.shape[1] if self.embeddings is not None else 0}).")
            except Exception as e:
                logger.error(f"Error loading vector store: {e}")
                self.embeddings = None
                self.metadata = []

    def cosine_similarity(self, vec_a: np.ndarray, mat_b: np.ndarray) -> np.ndarray:
        """
        Tính độ tương đồng Cosine giữa vector câu hỏi và ma trận vector các trang giáo trình:
        Cosine(a, b) = (a . b) / (||a|| * ||b||)
        """
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(mat_b, axis=1)
        # Tránh chia cho 0
        norm_b[norm_b == 0] = 1e-10
        if norm_a == 0:
            norm_a = 1e-10
        dot_product = np.dot(mat_b, vec_a)
        return dot_product / (norm_a * norm_b)

    def search_by_vector(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Truy vấn tìm kiếm Top-K trang có vector tương đồng ngữ nghĩa nhất"""
        if self.embeddings is None or len(self.metadata) == 0:
            return []

        q_vec = np.array(query_vector, dtype=np.float32)
        scores = self.cosine_similarity(q_vec, self.embeddings)
        
        # Lấy top k chỉ số có điểm cao nhất
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "page_number": self.metadata[idx]["page_number"],
                "similarity_score": round(float(scores[idx]), 4),
                "text": self.metadata[idx]["text"],
                "reference": f"PDF giáo trình, trang {self.metadata[idx]['page_number']}"
            })
        return results

    def save(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]):
        os.makedirs(settings.INDEX_DIR, exist_ok=True)
        arr = np.array(vectors, dtype=np.float32)
        np.save(self.vectors_file, arr)
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        self.embeddings = arr
        self.metadata = metadata
        logger.info(f"Saved {len(metadata)} page vectors to Vector Database.")

vector_store = VectorStore()
