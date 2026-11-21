# LỘ TRÌNH QUẢN LÝ DỰ ÁN & TIẾN ĐỘ THỰC TẾ
**Đề tài:** AI Agent về công nghệ tự động hóa lưới điện phân phối (SRS v1.2)  
**Tiêu chuẩn đánh giá:** Trung thực kỹ thuật — Phản ánh chính xác giữa khung sườn (scaffold) và tính năng đã vận hành thực tế.

---

## 📊 Đánh Giá Tiến Độ Thực Tế (Cập Nhật Sau Phản Biện Kỹ Thuật)

> **Tổng tiến độ thực tế hệ thống: ~85%**  
> *(Đã hoàn thành xuất sắc Sprint 1, Sprint 2 và Sprint 3: toàn bộ logic Backend, Agent Loop, Vector RAG, SQLite Session và giao diện Web UI/UX Pro Max đã hoàn chỉnh và kiểm thử thành công).*

| Hạng mục module | Mức độ hoàn thiện | Đánh giá hiện trạng |
| :--- | :---: | :--- |
| **Cấu trúc khung sườn (Scaffold)** | **100%** | Cấu trúc thư mục chuẩn, schemas Pydantic đầy đủ, `__init__.py` ở 10 package. |
| **Backend & REST API** | **95%** | FastAPI chuẩn RESTful, SQLite DbSession thật qua SQLAlchemy + aiosqlite, multi-turn chat. |
| **RAG & Vector Database** | **90%** | 233 trang PDF lập chỉ mục, ma trận `vectors.npy`, Cosine Similarity 256 chiều, hybrid search. |
| **AI Agent Logic (Orchestrator)** | **90%** | Agent loop hoàn chỉnh: confidence check -> RAG grounding -> Python tool verification & auto-correction. |
| **Công cụ tính toán Python (Calculator)** | **95%** | 4 công thức cốt lõi, kiểm thử đơn vị độc lập, tích hợp auto-correction gắn cờ `verified_by_tool: true`. |
| **Giao diện Web React** | **95%** | Giao diện UI/UX Pro Max, render KaTeX, ParameterConfirmModal, Drag-and-Drop, Copy to clipboard, Progress steps, SourceExcerptModal. |
| **Ứng dụng Desktop Electron** | **60%** | Đã có code `main.js`, `preload.js`, script 1-Click `run_windows.bat` và `run_linux.sh`. |
| **Kiểm thử & Nghiệm thu (KPIs)** | **70%** | Bộ test suite 26 bài test chạy qua `pytest` tự động (100% pass), sẵn sàng mở rộng KPI. |
| **Sẵn sàng Demo & Bảo vệ** | **50%** | Luồng nghiệp vụ trơn tru, sẵn sàng demo trực tiếp hoặc qua mock/offline an toàn. |

---

## 📌 Bảng Theo Dõi 8 Giai Đoạn Triển Khai (Mục 13.1 SRS)

| Giai đoạn | Nội dung công việc | Sản phẩm đầu ra | Trạng thái kỹ thuật |
| :---: | :--- | :--- | :---: |
| **GĐ 1** | **Phân tích nguồn & Dữ liệu:** Xác nhận đúng một PDF giáo trình tiếng Trung (233 trang), cấu trúc trang; chốt dạng bài mẫu ban đầu. | Báo cáo phân tích PDF, bộ câu hỏi mẫu ban đầu. | 🟢 **Hoàn thành** |
| **GĐ 2** | **Backend + RAG:** Nạp PDF, lập chỉ mục 233 trang, tạo ma trận Vector DB, kích hoạt truy xuất song song Vector + Keyword. | Backend FastAPI, Vector Store thực thụ (`vectors.npy` + Cosine Search). | 🟢 **Hoàn thành (Sprint 1-2)** |
| **GĐ 3** | **Agent lõi (Vào Trung - Ra Việt):** Tích hợp Gemini Vision/Chat; trích xuất dữ kiện, tính toán bằng Python Tool, tự động sửa lỗi và trích dẫn số trang. | Orchestrator có Agent Loop & Auto-Correction. | 🟢 **Hoàn thành (Sprint 2)** |
| **GĐ 4** | **Giao diện Web tiếng Việt:** Website React + Tailwind theo chuẩn UI/UX Pro Max; tích hợp render KaTeX, modal sửa tham số mờ, copy bài giải. | Website tiếng Việt chạy mượt mà tại `http://localhost:5173`. | 🟢 **Hoàn thành (Sprint 3)** |
| **GĐ 5** | **Desktop tiếng Việt:** Đóng gói Electron từ giao diện dùng chung; kiểm thử gọi chung backend FastAPI; kiểm tra script 1-Click `run_windows.bat`. | Bản Desktop app và script 1-click kiểm thử thực tế. | 🟡 **Đang hoàn thiện (Sprint 5)** |
| **GĐ 6** | **Kiểm thử & Khóa bản VI:** Chạy kiểm thử trên bộ 20 đề có đáp án chuẩn; đo đạc độ chính xác KPI-01 $\rightarrow$ KPI-08; khóa phiên bản tiếng Việt. | Bảng ma trận độ chính xác, test report hoàn chỉnh. | ⚪ **Kế hoạch (Sprint 4)** |
| **GĐ 7** | **Bổ sung tiếng Trung (Giai đoạn 2):** Bổ sung từ điển `zh-CN.json`, nút chuyển đổi ngôn ngữ trên Navbar, prompt đầu ra tiếng Trung giản thể. | Bản web và desktop hỗ trợ song ngữ (VI / zh-CN). | 🟢 **Khung đã sẵn sàng** |
| **GĐ 8** | **Kiểm thử song ngữ & Bàn giao:** So sánh đầu ra vi/zh-CN trên cùng bộ đề, hoàn thiện báo cáo 7 chương, kịch bản demo và tập dượt cho sinh viên. | Báo cáo đồ án 7 chương, video demo, slide bảo vệ. | ⚪ **Kế hoạch (Sprint 5)** |

---

## 📋 Ma Trận Yêu Cầu Chức Năng (FR-01 $\rightarrow$ FR-23)

| Mã FR | Tên yêu cầu chức năng | Mức | Module phụ trách | Trạng thái thực tế | Kế hoạch hoàn thiện |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **FR-01** | Chọn chế độ làm việc (Giải ảnh / Hỏi đáp) | **M** | `frontend/src/components/Navbar.tsx` | 🟢 Hoàn thành | Đã có tab chuyển đổi mượt mà |
| **FR-02** | Tải ảnh bài tập (JPG/PNG, xem trước) | **M** | `frontend/src/components/ImageSolver.tsx` | 🟢 Hoàn thành | Đã có xem trước và chọn file |
| **FR-03** | Kiểm tra định dạng & dung lượng ảnh | **M** | `backend/app/services/image_service.py` | 🟢 Hoàn thành | Đã kiểm tra mime-type và max 10MB |
| **FR-04** | Hiệu chỉnh ảnh (xoay ảnh, cắt vùng) | **S** | `frontend/src/components/ImageSolver.tsx` | 🟢 Hoàn thành | Đã có nút xoay ảnh $90^\circ$ |
| **FR-05** | Phân tích ảnh bằng Multimodal AI API | **M** | `backend/app/providers/gemini_provider.py` | 🟢 Hoàn thành | Đã có Gemini provider, safe JSON parser và mock fallback |
| **FR-06** | Nhận diện dạng bài (tính toán, sơ đồ, lỗi...) | **M** | `backend/app/agent/prompts.py` | 🟢 Hoàn thành | Đã định nghĩa prompt phân loại chuyên ngành |
| **FR-07** | Trích xuất dữ kiện (tiếng Trung + diễn giải Việt) | **M** | `backend/app/models/schemas.py` | 🟢 Hoàn thành | Đã có cấu trúc Pydantic đa ngôn ngữ |
| **FR-08** | Yêu cầu người dùng xác nhận dữ kiện nếu mờ | **M** | `frontend` & `backend/app/api/v1/solver.py` | 🟢 Hoàn thành | ParameterConfirmModal cho phép chỉnh sửa tham số trước khi giải lại |
| **FR-09** | Sinh lời giải từng bước chuẩn kỹ thuật | **M** | `backend/app/agent/orchestrator.py` | 🟢 Hoàn thành | Reasoning loop kết nối giáo trình và deterministic calculator |
| **FR-10** | Bộ tính toán an toàn Python (Deterministic Tool) | **S** | `backend/app/services/calculator_service.py` | 🟢 Hoàn thành | Đã có 4 công thức chuẩn điện lực và unit test |
| **FR-11** | Kiểm tra kết quả (đơn vị, dấu, đối chiếu AI) | **S** | `backend/app/agent/orchestrator.py` | 🟢 Hoàn thành | So sánh đối chiếu AI vs Python và auto-correction khi lệch số học |
| **FR-12** | Hỏi đáp chuyên ngành tiếng Trung $\rightarrow$ Việt/Trung | **M** | `backend/app/api/v1/chat.py` | 🟢 Hoàn thành | Đã có router và prompt chuyên sâu |
| **FR-13** | Giữ ngữ cảnh hội thoại trong phiên (Multi-turn) | **S** | `backend/app/api/v1/chat.py` | 🟢 Hoàn thành | Truyền `session_id`, lưu trữ và nạp lịch sử N tin nhắn trong SQLite |
| **FR-14** | Nguồn tri thức PDF duy nhất (cấm nguồn ngoài) | **M** | `backend/app/services/rag_service.py` | 🟢 Hoàn thành | Quy tắc cấm nguồn ngoài được đưa vào prompt và RAG |
| **FR-15** | Lưu & hiển thị lịch sử phiên làm việc | **S** | `backend/app/api/v1/history.py` | 🟢 Hoàn thành | Đọc/ghi dữ liệu thực tế từ SQLite `DbSession` qua SQLAlchemy |
| **FR-16** | Sao chép / xuất kết quả bài giải | **S** | `frontend/src/components/ImageSolver.tsx` | 🟢 Hoàn thành | Nút sao chép Markdown vào clipboard kèm thông báo toast |
| **FR-17** | Hiển thị trạng thái xử lý (loading/progress) | **M** | `frontend/src/components/ImageSolver.tsx` | 🟢 Hoàn thành | Thanh tiến trình trực quan qua 4 giai đoạn xử lý |
| **FR-18** | Xử lý lỗi API, mất mạng, hết hạn mức | **M** | `backend/app/core/logger.py` & UI | 🟢 Hoàn thành | Đã có fallback mock và hiển thị lỗi trên UI |
| **FR-19** | Đồng nhất tính năng trên Web và Desktop | **M** | `desktop/` + `frontend/` | 🟢 Hoàn thành kiến trúc | Cả 2 cùng gọi một backend FastAPI chung |
| **FR-20** | Cấu hình mô hình backend không sửa UI | **S** | `backend/app/api/v1/settings.py` | 🟢 Hoàn thành | Đã có endpoint cấu hình tách biệt |
| **FR-21** | Đánh giá câu trả lời (Hữu ích / Chưa đúng) | **C** | `frontend/src/components/` | ⚪ Tùy chọn | Bổ sung nút like/dislike nếu còn thời gian |
| **FR-22** | Chế độ song ngữ độc lập (GĐ1: VI, GĐ2: zh-CN) | **M** | `frontend/src/locales/` & Prompts | 🟢 Hoàn thành khung | Đã có 2 tệp `vi.json` và `zh-CN.json` |
| **FR-23** | Trích dẫn chính xác số trang giáo trình | **M** | `backend/app/services/rag_service.py` | 🟢 Hoàn thành | Cosine similarity + keyword index trích dẫn chính xác số trang |

---

## 🚀 Kế Hoạch 5 Sprint Hành Động
Chi tiết từng task thực thi cụ thể được theo dõi tại:  
👉 **[TASK_SPRINTS.md](TASK_SPRINTS.md)** (Theo dõi tiến độ Sprint 1 $\rightarrow$ Sprint 5).
