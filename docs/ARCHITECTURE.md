# Kiến trúc Hệ thống AI Agent Tự động hóa Lưới điện Phân phối

## 1. Sơ đồ Kiến trúc Tổng thể (Logical Architecture)

```
[Người dùng / Giảng viên]
            │
  ┌─────────┴─────────┐
  ▼                   ▼
Ứng dụng Desktop     Website
 (Electron App)    (React + Vite)
  └─────────┬─────────┘
            │  (REST API qua HTTP/JSON)
            ▼
┌──────────────────────────────────────────────┐
│        API BACKEND (Python FastAPI)          │
│  - Endpoint /solver/solve-image              │
│  - Endpoint /chat                            │
│  - Endpoint /history & /settings             │
└───────────────┬──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│         AI AGENT ORCHESTRATOR                │
│  ┌─────────────────────────────────────────┐ │
│  │ 1. Xử lý ảnh (Pillow/OpenCV)            │ │
│  │    Xoay, tăng tương phản, kiểm tra mờ   │ │
│  ├─────────────────────────────────────────┤ │
│  │ 2. Multimodal Vision AI (Gemini)        │ │
│  │    Đọc đề tiếng Trung, sơ đồ & công thức│ │
│  ├─────────────────────────────────────────┤ │
│  │ 3. Bộ tính toán an toàn (Calculator)    │ │
│  │    Python Sympy / Math tính xác định    │ │
│  ├─────────────────────────────────────────┤ │
│  │ 4. Grounded RAG (Nguồn duy nhất)        │ │
│  │    PDF giáo trình tiếng Trung (233 tr.) │ │
│  │    Trích dẫn chính xác số trang         │ │
│  └─────────────────────────────────────────┘ │
└───────────────┬──────────────────────────────┘
                │
  ┌─────────────┼─────────────┐
  ▼             ▼             ▼
SQLite DB    Gemini API    PDF Index
(Lịch sử)   (Đa phương thức) (Trang 1-233)
```

## 2. Các thành phần chính

1. **Frontend / Desktop:**
   - Sử dụng chung một mã nguồn React + Tailwind CSS.
   - Bản Desktop được bao bọc bởi Electron, chạy độc lập không phụ thuộc trình duyệt ngoài.
   - Hỗ trợ chuyển đổi song ngữ: Tiếng Việt (`vi.json`) và Tiếng Trung giản thể (`zh-CN.json`).

2. **Multimodal Vision:**
   - Tiếp nhận ảnh chụp bài tập thực tế từ giảng viên (tiếng Trung).
   - Tách bạch: Văn bản gốc tiếng Trung $\rightarrow$ Bản dịch tiếng Việt $\rightarrow$ Bảng thông số kỹ thuật.
   - Cho phép người dùng xác nhận thông số mờ trước khi chạy tính toán (FR-08).

3. **Grounded RAG (Single-Source):**
   - Chỉ sử dụng duy nhất tệp `backend/knowledge/course_textbook.pdf` (233 trang).
   - Tự động lập chỉ mục và lưu metadata `page_number` trong `backend/knowledge/index/pages.json`.
   - Mọi câu trả lời lý thuyết đều đính kèm `(PDF giáo trình, trang N)`.

4. **Deterministic Calculator Tool:**
   - Ngăn chặn triệt để hiện tượng AI ảo giác phép tính (LLM hallucination).
   - Module Python tính toán chuẩn: Tổn thất điện áp $\Delta U$, trào lưu công suất, dòng ngắn mạch $I_{sc}^{(3)}$, bù công suất phản kháng $Q_c$.
