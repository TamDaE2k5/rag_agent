# HỆ THỐNG QUẢN LÝ TASK DỰ ÁN (PROJECT TASK TRACKING)

Thư mục `task/` chứa toàn bộ danh sách công việc, tiến độ triển khai thực tế và tiêu chuẩn nghiệm thu của đồ án:
**"Xây dựng AI Agent về công nghệ tự động hóa lưới điện phân phối"** (Bám sát đặc tả SRS v1.2).

---

## 📑 Danh Sách Tài Liệu Quản Lý Task

1. 🚀 **[TASK_SPRINTS.md](TASK_SPRINTS.md):** **Kế hoạch hành động 5 Sprint chi tiết** (Từ phản biện kỹ thuật):
   - **Sprint 1:** "CẮM ĐIỆN" — Cài đặt môi trường, sửa `__init__.py`, chạy backend & frontend thực tế.
   - **Sprint 2:** "LÀM THẬT" — Kích hoạt Vector Search, Agent Reasoning Loop, Safe JSON Parser, Multi-turn Chat.
   - **Sprint 3:** "LÀM ĐẸP" — Tích hợp KaTeX render, UI sửa tham số mờ (FR-08), nút Copy (FR-16), Drag-and-Drop.
   - **Sprint 4:** "KIỂM THỬ" — Bộ 20 đề thi chuẩn, script đo đạc tự động KPI-01 $\rightarrow$ KPI-08.
   - **Sprint 5:** "ĐÓNG GÓI" — Electron Desktop, kịch bản demo 10 phút, bộ 10 câu hỏi phản biện bảo vệ đồ án.
2. 📌 **[TASK_ROADMAP.md](TASK_ROADMAP.md):** Bảng theo dõi tiến độ thực tế 8 giai đoạn và ma trận đối chiếu 23 yêu cầu chức năng (FR-01 đến FR-23) — *Đã cập nhật tỷ lệ hoàn thiện thực tế trung thực (~35%)*.
3. ⚙️ **[TASK_BACKEND_RAG.md](TASK_BACKEND_RAG.md):** Chi tiết các task thuộc về Backend FastAPI, Gemini API, Bộ tính toán an toàn Python và Vector Database.
4. 💻 **[TASK_FRONTEND_DESKTOP.md](TASK_FRONTEND_DESKTOP.md):** Chi tiết các task thuộc về Giao diện Web React + Tailwind CSS (UI/UX Pro Max), KaTeX Math và Ứng dụng Desktop Electron.
5. 📊 **[TASK_EVALUATION_DEMO.md](TASK_EVALUATION_DEMO.md):** Kế hoạch kiểm thử 20 đề bài tập chuẩn (KPI-03), kịch bản demo 10 phút trên lớp (Phụ lục B) và đề cương báo cáo 7 chương.

---

## 🛠 Nguyên Tắc Cập Nhật Tiến Độ
- **Trung thực kỹ thuật:** Chỉ đánh dấu hoàn thành `- [x]` khi tính năng đã được code, chạy thử và kiểm chứng hoạt động không lỗi (tránh đánh dấu hoàn thành trên khung sườn giả định).
- Mọi chỉnh sửa về nghiệp vụ cần được đối chiếu lại với tệp đặc tả [Dac_ta_do_an_AI_Agent_Tu_dong_hoa_luoi_dien_phan_phoi_v1.2.docx](../Dac_ta_do_an_AI_Agent_Tu_dong_hoa_luoi_dien_phan_phoi_v1.2.docx).
