import os
import sys
import json
import subprocess
from pathlib import Path

def ingest_pdf(pdf_path: str, output_json: str):
    print(f"Bắt đầu trích xuất và lập chỉ mục PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file {pdf_path}")
        return False

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    
    # Sử dụng pdftotext hoặc pypdf để trích xuất từng trang
    try:
        cmd = ["pdftotext", pdf_path, "-"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        full_text = result.stdout.decode("utf-8", errors="ignore")
        
        # Phân tách các trang bằng ký tự Form Feed (\x0c)
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
        
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump({
                "source": os.path.basename(pdf_path),
                "total_indexed_pages": len(pages_data),
                "pages": pages_data
            }, f, ensure_ascii=False, indent=2)
            
        print(f"Đã lập chỉ mục thành công {len(pages_data)} trang vào {output_json}")
        return True
    except Exception as e:
        print(f"Lỗi khi trích xuất PDF: {e}")
        return False

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    pdf = str(base_dir / "knowledge" / "course_textbook.pdf")
    out = str(base_dir / "knowledge" / "index" / "pages.json")
    ingest_pdf(pdf, out)
