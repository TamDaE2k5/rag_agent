# TASK CHI TIẾT: BACKEND, AI AGENT & VECTOR RAG

Mục tiêu: Đảm bảo tầng logic xử lý AI, tính toán kỹ thuật điện và truy xuất tài liệu vận hành ổn định, chính xác 100%.

---

## 1. Tầng Trí Tuệ Nhân Tạo & Điều Phối (AI Agent Orchestrator)
- [x] **T-BE-01:** Khởi tạo cấu trúc dự án FastAPI và cấu hình CORS đa nền tảng.
- [x] **T-BE-02:** Thiết kế Pydantic Schemas bám sát đặc tả SRS (ExtractedData, SolutionStep, SolutionResponse, ChatResponse).
- [x] **T-BE-03:** Viết adapter kết nối Google Gemini Vision API (`GeminiProvider`).
- [x] **T-BE-04:** Thiết kế Prompt hệ thống song ngữ chuyên ngành điện phân phối (VI & zh-CN).
- [x] **T-BE-05:** Xây dựng cơ chế Mock/Fallback để hệ thống không bị crash khi chưa điền API Key hoặc khi mất mạng.
- [ ] **T-BE-06:** Tối ưu hóa prompt để nhận diện các ký hiệu sơ đồ điện (biến dòng CT, máy cắt CB, Recloser, dao phân đoạn Sectionalizer, trạm biến áp phân phối).

---

## 2. Tầng Công Cụ Tính Toán Kỹ Thuật Điện (Deterministic Tools)
- [x] **T-CALC-01:** Viết hàm tính tổn thất điện áp đường dây 3 pha: $\Delta U = \frac{P \cdot R + Q \cdot X}{U_n}$.
- [x] **T-CALC-02:** Viết hàm tính tổn thất công suất tác dụng $\Delta P$ và phản kháng $\Delta Q$.
- [x] **T-CALC-03:** Viết hàm tính dòng ngắn mạch 3 pha đối xứng $I_{sc}^{(3)} = \frac{U_{tb}}{\sqrt{3} \cdot Z_{\Sigma}}$.
- [x] **T-CALC-04:** Viết hàm tính dung lượng bù công suất phản kháng $Q_c = P \cdot (\tan\varphi_1 - \tan\varphi_2)$.
- [x] **T-CALC-05:** Viết bộ kiểm thử đơn vị `test_calculator.py` chạy bằng Python `unittest`.
- [ ] **T-CALC-06:** Bổ sung thuật toán kiểm tra phối hợp thời gian bảo vệ quá dòng (đặc tính dốc phụ thuộc thời gian TCC theo chuẩn IEC).

---

## 3. Tầng Kho Tri Thức PDF & Vector Database (Grounded RAG)
- [x] **T-RAG-01:** Nạp tệp PDF giáo trình tiếng Trung 233 trang vào `backend/knowledge/course_textbook.pdf`.
- [x] **T-RAG-02:** Viết script `ingest_pdf.py` trích xuất toàn bộ văn bản 233 trang kèm số trang vào `pages.json`.
- [x] **T-RAG-03:** Xây dựng `VectorStore` nhúng (Embedded Vector DB) với ma trận vector đặc trưng ngữ nghĩa.
- [x] **T-RAG-04:** Cài đặt thuật toán đo khoảng cách Cosine Similarity để tìm trang có độ tương đồng cao nhất.
- [x] **T-RAG-05:** Cài đặt Hybrid Search (kết hợp Vector ngữ nghĩa + Keyword lọc mã thiết bị điện).
- [x] **T-RAG-06:** Khóa chặt quy tắc chỉ sử dụng nguồn duy nhất: cảnh báo rõ khi câu hỏi nằm ngoài giáo trình (FR-14).
