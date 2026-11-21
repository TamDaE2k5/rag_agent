# TASK CHI TIẾT: BACKEND, AI AGENT & VECTOR RAG

Mục tiêu: Đảm bảo tầng logic xử lý AI, tính toán kỹ thuật điện và truy xuất tài liệu vận hành ổn định, chính xác, có cơ chế tự kiểm chứng (Self-Correction).

---

## 1. Tầng Khởi Động & Môi Trường (System Infrastructure)
- [ ] **T-BE-00 (CRITICAL):** Tạo tệp `__init__.py` cho toàn bộ các thư mục con trong package Python (`backend/app/`, `api/`, `v1/`, `core/`, `models/`, `services/`, `providers/`, `agent/`, `tests/`) để tránh lỗi `ModuleNotFoundError`.
- [ ] **T-BE-00B (CRITICAL):** Chuẩn hóa `backend/requirements.txt`, gỡ bỏ `pydantic-settings`, cài đặt môi trường ảo và chạy `pip install` thành công.
- [x] **T-BE-01:** Khởi tạo cấu trúc dự án FastAPI và cấu hình CORS đa nền tảng.
- [x] **T-BE-02:** Thiết kế Pydantic Schemas bám sát đặc tả SRS (ExtractedData, SolutionStep, SolutionResponse, ChatResponse).

---

## 2. Tầng Trí Tuệ Nhân Tạo & Điều Phối (AI Agent Orchestrator)
- [x] **T-BE-03:** Viết adapter kết nối Google Gemini API (`GeminiProvider`).
- [ ] **T-BE-03B:** Bổ sung hàm `Safe JSON Parser` trong `GeminiProvider`: bóc tách khối Markdown JSON bằng regex, chống crash khi AI trả về văn bản kèm giải thích.
- [x] **T-BE-04:** Thiết kế Prompt hệ thống song ngữ chuyên ngành điện phân phối (VI & zh-CN).
- [x] **T-BE-05:** Xây dựng cơ chế Mock/Fallback để hệ thống không bị crash khi chưa có API Key hoặc khi mất mạng.
- [ ] **T-BE-06:** Tối ưu hóa prompt để nhận diện các ký hiệu sơ đồ điện (biến dòng CT, máy cắt CB, Recloser, dao phân đoạn Sectionalizer, trạm biến áp phân phối).
- [ ] **T-BE-07 (Agent Core):** Nâng cấp `AgentOrchestrator` từ pipeline tuần tự thành **Agent Reasoning & Verification Loop**:
  - Trích xuất dữ kiện $\rightarrow$ Đánh giá độ tin cậy ($confidence$).
  - Truy xuất RAG từ giáo trình để lấy phương pháp giải và công thức chuẩn.
  - Sử dụng Deterministic Calculator để tính toán độc lập.
  - Tự động so sánh đối chiếu kết quả giữa AI và Python (Auto-Correction) nếu có sai lệch số học.
- [ ] **T-BE-08:** Quản lý hội thoại đa lượt (Multi-turn Context - FR-13) trong `chat.py`: duy trì ngữ cảnh trao đổi liên tục dựa trên `session_id`.
- [ ] **T-BE-09:** Thay thế mock data trong `history.py` bằng thao tác đọc/ghi cơ sở dữ liệu SQLite thật (`DbSession` qua SQLAlchemy + aiosqlite - FR-15).

---

## 3. Tầng Công Cụ Tính Toán Kỹ Thuật Điện (Deterministic Tools)
- [x] **T-CALC-01:** Viết hàm tính tổn thất điện áp đường dây 3 pha: $\Delta U = \frac{P \cdot R + Q \cdot X}{U_n}$.
- [x] **T-CALC-02:** Viết hàm tính tổn thất công suất tác dụng $\Delta P$ và phản kháng $\Delta Q$.
- [x] **T-CALC-03:** Viết hàm tính dòng ngắn mạch 3 pha đối xứng $I_{sc}^{(3)} = \frac{U_{tb}}{\sqrt{3} \cdot Z_{\Sigma}}$.
- [x] **T-CALC-04:** Viết hàm tính dung lượng bù công suất phản kháng $Q_c = P \cdot (\tan\varphi_1 - \tan\varphi_2)$.
- [x] **T-CALC-05:** Viết bộ kiểm thử đơn vị `test_calculator.py` chạy bằng Python `unittest`.
- [ ] **T-CALC-06:** Mở rộng tích hợp các hàm tính toán vào quy trình tự động kiểm tra đáp số bài giải của Agent (FR-11).
- [ ] **T-CALC-07:** Bổ sung thuật toán kiểm tra phối hợp thời gian bảo vệ quá dòng (đặc tính dốc phụ thuộc thời gian TCC theo chuẩn IEC).

---

## 4. Tầng Kho Tri Thức PDF & Vector Database (Grounded RAG)
- [x] **T-RAG-01:** Nạp tệp PDF giáo trình tiếng Trung 233 trang vào `backend/knowledge/course_textbook.pdf`.
- [x] **T-RAG-02:** Viết script `ingest_pdf.py` trích xuất toàn bộ văn bản 233 trang kèm số trang vào `pages.json`.
- [x] **T-RAG-03:** Xây dựng `VectorStore` nhúng (Embedded Vector DB) với ma trận vector đặc trưng `vectors.npy`.
- [ ] **T-RAG-04 (HIGH):** Sửa lệnh `pass` rỗng tại dòng 73 trong `backend/app/services/rag_service.py`: kích hoạt thuật toán Cosine Similarity đối chiếu câu truy vấn với ma trận vector.
- [ ] **T-RAG-05:** Bổ sung tích hợp Google Embedding API (`models/text-embedding-004`) để nâng cao độ chính xác truy xuất ngữ nghĩa tiếng Trung vượt trội so với TF-IDF thô.
- [x] **T-RAG-06:** Khóa chặt quy tắc chỉ sử dụng nguồn duy nhất: từ chối và cảnh báo rõ khi câu hỏi nằm ngoài giáo trình (FR-14, FR-23).
