# API Documentation - AI Agent Tự động hóa Lưới điện Phân phối (v1.2)

Base URL: `http://127.0.0.1:8000/api/v1`

---

## 1. Giải bài tập qua ảnh (`/solver`)

### `POST /solver/solve-image`
Tiếp nhận ảnh chụp đề bài tiếng Trung, nhận diện sơ đồ và thông số, gọi Gemini Vision và bộ tính toán an toàn Python.

- **Content-Type:** `multipart/form-data`
- **Tham số:**
  - `file`: Tệp ảnh (JPG/PNG, tối đa 15MB).
  - `rotate_angle`: Góc xoay nếu ảnh chụp nghiêng (0, 90, 180, 270). Mặc định `0`.
  - `language`: Ngôn ngữ trả lời (`vi` cho Giai đoạn 1, `zh-CN` cho Giai đoạn 2).

#### Response (200 OK)
```json
{
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "status": "success",
  "problem_type": "calculation",
  "extracted_data": {
    "problem_type": "calculation",
    "raw_text_zh": "某10kV配电网线路，负荷P = 1200 kW, cos phi = 0.85...",
    "interpreted_text_vi": "Đường dây phân phối 10kV cấp điện cho phụ tải...",
    "parameters": [
      {"name": "Điện áp định mức", "symbol": "U_n", "value": 10.0, "unit": "kV", "is_confirmed": true}
    ],
    "unknowns": [
      {"symbol": "Delta U", "name": "Tổn thất điện áp", "unit": "V"}
    ],
    "assumptions": [],
    "confidence_score": 1.0,
    "requires_user_confirmation": false
  },
  "steps": [
    {
      "step_number": 1,
      "title": "Tính công suất phản kháng của phụ tải",
      "explanation": "Từ P và cos phi = 0.85...",
      "formula_latex": "Q = P \\cdot \\tan \\varphi",
      "calculated_value": "744.0 kvar",
      "verified_by_tool": true
    }
  ],
  "final_answer": "Tổn thất điện áp trên đường dây là 538.08 V (5.38%).",
  "unit": "V",
  "textbook_reference": "PDF giáo trình, trang 42",
  "warnings": [],
  "language": "vi"
}
```

---

## 2. Hỏi đáp chuyên ngành (`/chat`)

### `POST /chat`
Nhận câu hỏi văn bản tiếng Trung hoặc tiếng Việt, tra cứu trực tiếp từ file PDF giáo trình tiếng Trung duy nhất và trả về lời giải thích có số trang trích dẫn.

- **Content-Type:** `application/json`
- **Request Body:**
```json
{
  "question": "重合器（Recloser）的工作原理是什么？",
  "session_id": null,
  "language": "vi"
}
```

#### Response (200 OK)
```json
{
  "session_id": "4a2b918f-28c0-4fe7-873b-e2bfa7c9197a",
  "direct_answer": "Dao cắt tự đóng lại (Recloser) là thiết bị...",
  "explanation": "Recloser có khả năng phân biệt sự cố thoáng qua...",
  "course_relation": "Trong tự động hóa lưới điện phân phối, Recloser phối hợp với Dao phân đoạn...",
  "example": "Khi sét đánh làm phóng điện sứ trên xuất tuyến 22kV...",
  "textbook_reference": "PDF giáo trình, trang 140",
  "notes": "Lưu ý kiểm tra đường đặc tính TCC...",
  "language": "vi"
}
```

---

## 3. Lịch sử & Cấu hình

- `GET /history`: Danh sách các phiên đã lưu.
- `GET /settings`: Trạng thái mô hình AI, trạng thái chỉ mục PDF giáo trình.
- `GET /api/health`: Kiểm tra sức khỏe hệ thống (trả về `{"status": "healthy"}`).
