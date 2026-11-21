# LỘ TRÌNH QUẢN LÝ DỰ ÁN & TIẾN ĐỘ CÔNG VIỆC
**Đề tài:** AI Agent về công nghệ tự động hóa lưới điện phân phối (SRS v1.2)

---

## 📌 Bảng Theo Dõi 8 Giai Đoạn Triển Khai (Mục 13.1 SRS)

| Giai đoạn | Nội dung công việc | Sản phẩm đầu ra | Trạng thái |
| :---: | :--- | :--- | :---: |
| **GĐ 1** | **Phân tích nguồn & Dữ liệu:** Xác nhận đúng một PDF giáo trình tiếng Trung, cấu trúc trang, nội dung chữ/scan; chốt dạng bài mẫu và đáp án chuẩn. | Báo cáo phân tích PDF, bộ câu hỏi/đề mẫu ban đầu. | 🟢 **Hoàn thành** |
| **GĐ 2** | **Backend + RAG:** Nạp PDF duy nhất (233 trang), lập chỉ mục văn bản + ma trận Vector Database, truy xuất trực tiếp tiếng Trung; tạo API endpoints. | Backend FastAPI, Vector Store (`vectors.npy`) hoạt động. | 🟢 **Hoàn thành** |
| **GĐ 3** | **Agent lõi (Vào Trung - Ra Việt):** Tích hợp Gemini Vision/Chat; tạo prompt đọc đề ảnh và câu hỏi tiếng Trung, trích xuất dữ kiện, tính toán bằng Python Tool và sinh lời giải tiếng Việt. | Endpoint `/solver/solve-image` & `/chat` có trích dẫn số trang sách. | 🟢 **Hoàn thành** |
| **GĐ 4** | **Giao diện Web tiếng Việt:** Thiết kế website React + Tailwind theo chuẩn UI/UX Pro Max; kiểm tra luồng upload ảnh, xoay ảnh, xem trước và xem kết quả. | Website tiếng Việt hoàn chỉnh tại `http://localhost:5173`. | 🟢 **Hoàn thành** |
| **GĐ 5** | **Desktop tiếng Việt:** Đóng gói Electron từ giao diện dùng chung; kiểm thử gọi chung backend FastAPI; tạo script khởi động 1-Click `run_windows.bat`. | Bản Desktop app và script 1-click cho máy Windows. | 🟢 **Hoàn thành** |
| **GĐ 6** | **Kiểm thử & Khóa bản VI:** Chạy kiểm thử trên bộ đề có đáp án chuẩn; đo đạc độ chính xác bóc tách dữ kiện và tính toán; khóa phiên bản tiếng Việt. | Bản tiếng Việt ổn định, test report ban đầu. | 🟡 **Đang tiến hành** |
| **GĐ 7** | **Bổ sung tiếng Trung (Giai đoạn 2):** Bổ sung file từ điển `zh-CN.json`, nút chuyển đổi ngôn ngữ trên Navbar, prompt đầu ra tiếng Trung giản thể. | Bản web và desktop hỗ trợ song ngữ (VI / zh-CN). | 🟢 **Hoàn thành khung** |
| **GĐ 8** | **Kiểm thử song ngữ & Bàn giao:** So sánh đầu ra vi/zh-CN trên cùng bộ đề, hoàn thiện báo cáo 7 chương, kịch bản demo và tập dượt cho sinh viên. | Báo cáo đồ án 7 chương, mã nguồn, video demo. | ⚪ **Chưa bắt đầu** |

---

## 📋 Ma Trận Yêu Cầu Chức Năng (FR-01 $\rightarrow$ FR-23)

| Mã FR | Tên yêu cầu | Mức ưu tiên | Module phụ trách | Trạng thái |
| :--- | :--- | :---: | :--- | :---: |
| **FR-01** | Chọn chế độ làm việc (Giải ảnh / Hỏi đáp) | **M** | `frontend/src/components/Navbar.tsx` | ✅ Đã có |
| **FR-02** | Tải ảnh bài tập (JPG/PNG, xem trước) | **M** | `frontend/src/components/ImageSolver.tsx` | ✅ Đã có |
| **FR-03** | Kiểm tra định dạng & dung lượng ảnh | **M** | `backend/app/services/image_service.py` | ✅ Đã có |
| **FR-04** | Hiệu chỉnh ảnh (xoay ảnh, cắt vùng) | **S** | `frontend/src/components/ImageSolver.tsx` | ✅ Đã có |
| **FR-05** | Phân tích ảnh bằng Multimodal AI API | **M** | `backend/app/providers/gemini_provider.py` | ✅ Đã có |
| **FR-06** | Nhận diện dạng bài (tính toán, sơ đồ, lỗi...) | **M** | `backend/app/agent/prompts.py` | ✅ Đã có |
| **FR-07** | Trích xuất dữ kiện (tiếng Trung + diễn giải Việt) | **M** | `backend/app/models/schemas.py` | ✅ Đã có |
| **FR-08** | Yêu cầu người dùng xác nhận dữ kiện nếu mờ | **M** | `backend/app/api/v1/solver.py` | ✅ Đã có |
| **FR-09** | Sinh lời giải từng bước chuẩn kỹ thuật | **M** | `backend/app/agent/orchestrator.py` | ✅ Đã có |
| **FR-10** | Bộ tính toán an toàn Python (Deterministic Tool) | **S** | `backend/app/services/calculator_service.py` | ✅ Đã có |
| **FR-11** | Kiểm tra kết quả (đơn vị, dấu, tính nhất quán) | **S** | `backend/app/services/calculator_service.py` | ✅ Đã có |
| **FR-12** | Hỏi đáp chuyên ngành tiếng Trung $\rightarrow$ Việt/Trung | **M** | `backend/app/api/v1/chat.py` | ✅ Đã có |
| **FR-13** | Giữ ngữ cảnh hội thoại trong phiên | **S** | `backend/app/api/v1/chat.py` | ✅ Đã có |
| **FR-14** | Nguồn tri thức PDF duy nhất (cấm nguồn ngoài) | **M** | `backend/app/services/rag_service.py` | ✅ Đã có |
| **FR-15** | Lưu & hiển thị lịch sử phiên | **S** | `backend/app/api/v1/history.py` | ✅ Đã có |
| **FR-16** | Sao chép / xuất kết quả bài giải | **S** | `frontend/src/components/ImageSolver.tsx` | 🟡 Cần bổ sung nút copy |
| **FR-17** | Hiển thị trạng thái xử lý (loading/progress) | **M** | `frontend/src/components/ImageSolver.tsx` | ✅ Đã có |
| **FR-18** | Xử lý lỗi API, mất mạng, hết hạn mức | **M** | `backend/app/core/logger.py` & UI Error alert | ✅ Đã có |
| **FR-19** | Đồng nhất tính năng trên Web và Desktop | **M** | Electron wrapper + React frontend | ✅ Đã có |
| **FR-20** | Cấu hình mô hình backend không sửa UI | **S** | `backend/app/api/v1/settings.py` | ✅ Đã có |
| **FR-21** | Đánh giá câu trả lời (Hữu ích / Chưa đúng) | **C** | Frontend feedback buttons | ⚪ Chưa làm |
| **FR-22** | Chế độ song ngữ độc lập (GĐ1: VI, GĐ2: zh-CN) | **M** | `frontend/src/locales/` & Gemini prompt | ✅ Đã có |
| **FR-23** | Trích dẫn chính xác số trang giáo trình | **M** | `backend/app/services/vector_store.py` | ✅ Đã có |
