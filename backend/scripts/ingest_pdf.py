import os
import sys
import json
import math
import subprocess
from collections import Counter
from pathlib import Path
import numpy as np

def ingest_pdf(pdf_path: str, index_dir: str):
    print(f"Bắt đầu trích xuất và lập chỉ mục PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file {pdf_path}")
        return False

    os.makedirs(index_dir, exist_ok=True)
    pages_json = os.path.join(index_dir, "pages.json")
    vectors_npy = os.path.join(index_dir, "vectors.npy")
    metadata_json = os.path.join(index_dir, "vector_metadata.json")

    # 1. Trích xuất từng trang
    try:
        cmd = ["pdftotext", pdf_path, "-"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        full_text = result.stdout.decode("utf-8", errors="ignore")
        raw_pages = full_text.split("\x0c")
        
        pages_data = []
        for i, page_text in enumerate(raw_pages):
            clean_text = page_text.strip()
            if clean_text:
                pages_data.append({
                    "page_number": i + 1,
                    "text": clean_text,
                    "char_count": len(clean_text)
                })
        
        with open(pages_json, "w", encoding="utf-8") as f:
            json.dump({
                "source": os.path.basename(pdf_path),
                "total_indexed_pages": len(pages_data),
                "pages": pages_data
            }, f, ensure_ascii=False, indent=2)
            
        print(f"[1/2] Đã lập chỉ mục văn bản {len(pages_data)} trang vào {pages_json}")

        # 2. Xây dựng Vector Database (Embedding Space)
        corpus = [p["text"] for p in pages_data]
        vocab = Counter()
        for doc in corpus:
            for i in range(len(doc) - 1):
                bigram = doc[i:i+2]
                if '\u4e00' <= bigram[0] <= '\u9fff' and '\u4e00' <= bigram[1] <= '\u9fff':
                    vocab[bigram] += 1

        top_vocab = [term for term, count in vocab.most_common(256)]
        dim = len(top_vocab)
        vectors = []
        for doc in corpus:
            v = np.zeros(dim, dtype=np.float32)
            for i, term in enumerate(top_vocab):
                count = doc.count(term)
                if count > 0:
                    v[i] = 1.0 + math.log(count)
            norm = np.linalg.norm(v)
            if norm > 0:
                v = v / norm
            vectors.append(v)

        arr = np.array(vectors, dtype=np.float32)
        np.save(vectors_npy, arr)
        metadata = [{"page_number": p["page_number"], "text": p["text"][:1200]} for p in pages_data]
        with open(metadata_json, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"[2/2] Đã tạo thành công Vector Database {arr.shape} vào {vectors_npy}")
        return True
    except Exception as e:
        print(f"Lỗi khi xử lý PDF: {e}")
        return False

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    pdf = str(base_dir / "knowledge" / "course_textbook.pdf")
    idx_dir = str(base_dir / "knowledge" / "index")
    ingest_pdf(pdf, idx_dir)
