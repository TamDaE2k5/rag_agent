# KẾ HOẠCH THỰC HIỆN 5 SPRINT (TỪ PHẢN BIỆN KỸ THUẬT)

> **Triết lý thực thi:** *"Make it work → Make it correct → Make it pretty → Make it provable"*  
> **Mục tiêu:** Đưa dự án từ trạng thái **Scaffold (~35%)** lên **Hoàn thiện 100%**, có thể chạy mượt mà trên máy tính của bạn sinh viên không chuyên IT và bảo vệ đạt điểm cao trước hội đồng.

---

## 🏃 Sprint 1: "CẮM ĐIỆN" — Khởi Chạy Hệ Thống Thực Tế
- **Mục tiêu:** Hệ thống khởi động được, backend và frontend giao tiếp thành công, test API thật không dùng mock.
- **Thời lượng dự kiến:** 1 - 2 ngày
- **Mức độ ưu tiên:** 🚨 **CRITICAL**

### Danh sách công việc:
- [ ] **S1.1 - Khởi tạo package Python:** Bổ sung `__init__.py` vào toàn bộ các thư mục package (`backend/`, `backend/app/`, `backend/app/api/`, `backend/app/api/v1/`, `backend/app/core/`, `backend/app/models/`, `backend/app/services/`, `backend/app/providers/`, `backend/app/agent/`, `backend/app/tests/`).
- [ ] **S1.2 - Chuẩn hóa dependencies:** Làm sạch `backend/requirements.txt`:
  - Loại bỏ `pydantic-settings` (đã viết code custom parser nhẹ hơn).
  - Chuẩn hóa thư viện Google GenAI (dùng `google-genai` hoặc `google-generativeai` thống nhất).
  - Đảm bảo `fastapi`, `uvicorn`, `pillow`, `sqlalchemy`, `aiosqlite`, `python-multipart` được cài đặt chuẩn xác.
- [ ] **S1.3 - Cài đặt môi trường Backend:** Chạy `pip install -r backend/requirements.txt` trong virtual environment.
- [ ] **S1.4 - Cài đặt môi trường Frontend:** Chạy `npm install` tại thư mục `frontend/`.
- [ ] **S1.5 - Cấu hình API Key:** Tạo file `backend/.env` với `GEMINI_API_KEY` thực tế (lấy từ Google AI Studio miễn phí).
- [ ] **S1.6 - Khởi động kiểm thử Backend:** Chạy `uvicorn backend.app.main:app --port 8000` và kiểm tra endpoint `/api/health`.
- [ ] **S1.7 - Khởi động kiểm thử Frontend:** Chạy `npm run dev` tại `frontend/` và kiểm tra giao diện trên trình duyệt `http://localhost:5173`.
- [ ] **S1.8 - E2E Smoke Test:** Tải ảnh mẫu `sample-data/questions/anh_bai_tap_mau.jpeg` lên giao diện, kiểm tra luồng nhận diện và trả kết quả thật từ Gemini.

---

## 🧠 Sprint 2: "LÀM THẬT" — Hoàn Thiện Logic Cốt Lõi & Agent Loop
- **Mục tiêu:** Biến hệ thống từ pipeline tuần tự đơn giản thành AI Agent thực thụ (có reasoning, kiểm chứng toán học, RAG vector thật, lưu trữ phiên).
- **Thời lượng dự kiến:** 2 - 3 ngày
- **Mức độ ưu tiên:** ⚠️ **HIGH**

### Danh sách công việc:
- [ ] **S2.1 - Kích hoạt Vector Search thực thụ (FR-23):**
  - Xóa bỏ lệnh `pass` rỗng tại dòng 73 `backend/app/services/rag_service.py`.
  - Triển khai tính toán cosine similarity giữa câu truy vấn và ma trận `vectors.npy` (233 trang).
  - Tích hợp thêm phương án Google Embedding API (`models/text-embedding-004`) để hiểu ngữ nghĩa tiếng Trung sâu hơn.
- [ ] **S2.2 - Xây dựng Agent Reasoning & Verification Loop:**
  - Nâng cấp `AgentOrchestrator`:
    1. *Bước 1 - Vision Extraction:* Trích xuất đề bài, sơ đồ và thông số kèm độ tin cậy (`confidence`).
    2. *Bước 2 - Confidence Check (FR-08):* Nếu thông số mờ/không chắc chắn, trả về yêu cầu người dùng xác nhận.
    3. *Bước 3 - RAG Retrieval:* Truy xuất phương pháp giải và công thức chuẩn từ PDF giáo trình.
    4. *Bước 4 - Deterministic Calculator Verification (FR-10, FR-11):* Dùng Python tính toán độc lập, đối chiếu kết quả của AI vs. Python.
    5. *Bước 5 - Auto-Correction:* Nếu AI tính nhầm số học, tự động sửa bằng giá trị chuẩn từ Python và gắn cờ `verified_by_tool: true`.
- [ ] **S2.3 - Bộ phân tích JSON an toàn (`Safe JSON Parser`):**
  - Viết hàm bóc tách JSON chống crash trong `GeminiProvider`: hỗ trợ regex lọc khối ` ```json ... ``` ` và tự sửa lỗi cú pháp phổ biến của LLM.
- [ ] **S2.4 - Ngữ cảnh hội thoại đa lượt (Multi-turn Chat Context - FR-13):**
  - Cập nhật `backend/app/api/v1/chat.py` nhận `session_id`, lưu trữ và nạp lịch sử N tin nhắn gần nhất để duy trì ngữ cảnh trao đổi.
- [ ] **S2.5 - Lưu trữ lịch sử phiên thực tế vào SQLite (FR-15):**
  - Thay thế mock data cứng trong `backend/app/api/v1/history.py` bằng thao tác đọc/ghi cơ sở dữ liệu `DbSession` qua SQLAlchemy + aiosqlite.

---

## 🎨 Sprint 3: "LÀM ĐẸP" — Trải Nghiệm Người Dùng (UI/UX Pro Max)
- **Mục tiêu:** Giao diện trực quan, công thức toán hiển thị chuẩn KaTeX, thao tác kéo thả mượt mà, hỗ trợ bạn sinh viên demo dễ dàng.
- **Thời lượng dự kiến:** 1 - 2 ngày
- **Mức độ ưu tiên:** 🟡 **MEDIUM**

### Danh sách công việc:
- [ ] **S3.1 - Render công thức toán KaTeX:**
  - Thay thế chuỗi raw LaTeX text tại `ImageSolver.tsx` bằng component hiển thị KaTeX (`katex.renderToString` hoặc thẻ chứa KaTeX).
- [ ] **S3.2 - Giao diện xác nhận tham số đề bài (FR-08):**
  - Thêm modal/bảng cho phép sinh viên click chỉnh sửa trực tiếp giá trị các đại lượng ($P, Q, cos\varphi, R, X, U$) trước khi bấm giải lại.
- [ ] **S3.3 - Nút sao chép lời giải ra Clipboard (FR-16):**
  - Thêm nút "Sao chép lời giải" (dạng văn bản / Markdown định dạng đẹp) kèm thông báo toast thành công.
- [ ] **S3.4 - Kéo thả ảnh thực sự (Drag-and-Drop):**
  - Bổ sung các event handler `onDragOver`, `onDragLeave`, `onDrop` cho khung tải ảnh bài tập.
- [ ] **S3.5 - Hiển thị trạng thái xử lý từng bước (Progress Steps - FR-17):**
  - Hiển thị tiến trình trực quan: *"Đang tiền xử lý ảnh..."* $\rightarrow$ *"Đang trích xuất dữ kiện..."* $\rightarrow$ *"Đang tra cứu giáo trình..."* $\rightarrow$ *"Đang kiểm chứng tính toán..."*.
- [ ] **S3.6 - Hộp xem trích dẫn sách (PDF Excerpt Modal):**
  - Khi click vào huy hiệu "PDF giáo trình, trang X", mở popup hiển thị nguyên văn đoạn trích tiếng Trung và bản dịch tiếng Việt từ trang sách đó.
- [ ] **S3.7 - Chat UX hoàn thiện:**
  - Thêm hiệu ứng gõ phím / typing spinner khi AI đang phản hồi; nút xóa lịch sử chat phiên làm việc.

---

## 📊 Sprint 4: "KIỂM THỬ & ĐO LƯỜNG" — Chứng Minh Độ Chính Xác (KPIs)
- **Mục tiêu:** Thu thập số liệu thực tế đo lường KPI-01 đến KPI-08, lập bảng ma trận đánh giá để đưa vào báo cáo và slide bảo vệ.
- **Thời lượng dự kiến:** 1 - 2 ngày
- **Mức độ ưu tiên:** ⚠️ **HIGH (Quyết định điểm số)**

### Danh sách công việc:
- [ ] **S4.1 - Mở rộng bộ đề kiểm thử (Test Suite - KPI-03):**
  - Xây dựng đủ 20 bài tập thực tế từ giáo trình tiếng Trung phân loại theo 4 nhóm dạng bài chính:
    1. Tính toán sụt áp và tổn thất công suất đường dây ($\Delta U, \Delta P, \Delta Q$).
    2. Tính toán dòng ngắn mạch 3 pha đối xứng và chọn thiết bị bảo vệ.
    3. Tính toán dung lượng bù công suất phản kháng $Q_c$.
    4. Phối hợp bảo vệ Recloser và Sectionalizer (bài tập nguyên lý / sơ đồ).
- [ ] **S4.2 - Chạy đánh giá tự động (Automated Evaluation):**
  - Viết script Python chạy tự động qua 20 test case, ghi nhận kết quả và đo đạc:
    - Tỷ lệ bóc tách dữ kiện chính xác (Mục tiêu KPI-01: $\ge 85\%$).
    - Sai số tính toán so với đáp án chuẩn (Mục tiêu KPI-02: $\le 2\%$).
    - Thời gian phản hồi trung bình (Mục tiêu KPI-05: $\le 15s$).
    - Tỷ lệ trích dẫn đúng trang sách giáo trình (Mục tiêu KPI-04: $\ge 80\%$).
- [ ] **S4.3 - Kiểm thử kịch bản ngoại lệ (Edge Cases):**
  - Thử nghiệm ảnh bị mờ, ảnh chụp nghiêng góc $90^\circ$, ảnh sơ đồ vẽ tay, đề bài ngoài phạm vi môn học (đảm bảo hệ thống từ chối lịch sự theo FR-14).
- [ ] **S4.4 - Xuất báo cáo kiểm thử:**
  - Tổng hợp số liệu thành bảng Markdown và file CSV/Excel phục vụ đưa trực tiếp vào Chương 6 của Báo cáo đồ án.

---

## 📦 Sprint 5: "ĐÓNG GÓI & DIỄN TẬP" — Bàn Giao Không Lỗi Cho Sinh Viên
- **Mục tiêu:** Đảm bảo bạn sinh viên không chuyên IT mở máy lên là chạy được ngay, diễn tập thành thạo 10 phút demo và trả lời trôi chảy câu hỏi phản biện.
- **Thời lượng dự kiến:** 1 ngày
- **Mức độ ưu tiên:** 🚨 **CRITICAL**

### Danh sách công việc:
- [ ] **S5.1 - Hoàn thiện ứng dụng Desktop Electron:**
  - Chạy thử nghiệm và sửa lỗi tích hợp giữa Electron và giao diện React build tĩnh (`dist/`).
  - Kiểm tra script `run_windows.bat` và `run_linux.sh` đảm bảo tự động khởi động cả backend lẫn giao diện chỉ với 1 cú click chuột.
- [ ] **S5.2 - Kịch bản Demo 10 phút (Theo Phụ lục B SRS):**
  - Soạn sẵn kịch bản từng phút:
    - Phút 01-02: Giới thiệu giao diện song ngữ, mục tiêu đề tài.
    - Phút 03-05: Demo giải bài tập ảnh tiếng Trung số 1 (Tính sụt áp $\Delta U$, chỉ ra công cụ Python kiểm chứng).
    - Phút 06-07: Demo giải bài tập số 2 (Phối hợp bảo vệ Recloser, trích dẫn trang sách).
    - Phút 08-09: Demo hỏi đáp chuyên ngành RAG (hỏi về nguyên lý FA, kiểm tra trích dẫn số trang).
    - Phút 10: Tóm tắt hiệu quả và mở phần Q&A.
- [ ] **S5.3 - Bộ 10 câu hỏi phản biện & đáp án cho sinh viên:**
  - Chuẩn bị tài liệu hỏi-đáp "tủ" cho sinh viên:
    1. *Hệ thống khác gì ChatGPT thông thường?* (RAG từ 1 sách duy nhất, có Python Deterministic Tool, trích dẫn chính xác số trang).
    2. *Vector Database hoạt động như thế nào trong bài này?*
    3. *Nếu ảnh chụp bị mờ thì AI xử lý ra sao?*
    4. *Cơ chế kiểm chứng Python hoạt động ở bước nào?*
    5. *... (kèm đáp án ngắn gọn, đúng chuyên ngành).*
- [ ] **S5.4 - Dự thảo Khung Báo Cáo Đồ Án 7 Chương:**
  - Viết dàn ý chi tiết và nội dung các chương báo cáo theo đúng cấu trúc Mục 15.1 SRS.
