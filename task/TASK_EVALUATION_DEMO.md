# TASK CHI TIẾT: KIỂM THỬ, BỘ ĐỀ MẪU & BẢO VỆ ĐỒ ÁN

Mục tiêu: Đạt chỉ số chất lượng KPI-01 $\rightarrow$ KPI-08, chuẩn bị kịch bản demo 10 phút và tài liệu bàn giao để sinh viên đạt điểm tuyệt đối.

---

## 1. Bộ Dữ Liệu Kiểm Thử Chuẩn (Test Suite - KPI-03)
- [x] **T-QA-01:** Tạo thư mục `sample-data/questions/` và `sample-data/answer-key/`.
- [x] **T-QA-02:** Đưa ảnh bài tập mẫu tiếng Trung thực tế (`anh_bai_tap_mau.jpeg`) vào bộ đề test.
- [x] **T-QA-03:** Xây dựng file mô tả kịch bản test `test_suite.json` ban đầu (3 đề mẫu).
- [ ] **T-QA-04:** Thu thập và chuẩn hóa đủ 20 đề bài tập từ giáo trình tiếng Trung có đáp án đối chiếu để đạt chỉ tiêu nghiệm thu (KPI-03):
  - Dạng 1: Tính toán sụt áp và tổn thất công suất đường dây ($\Delta U, \Delta P, \Delta Q$).
  - Dạng 2: Tính toán dòng ngắn mạch 3 pha đối xứng $I_{sc}^{(3)}$ và chọn thiết bị bảo vệ.
  - Dạng 3: Tính toán dung lượng bù công suất phản kháng $Q_c$.
  - Dạng 4: Phối hợp bảo vệ Recloser và Sectionalizer (sơ đồ nguyên lý).
- [ ] **T-QA-05:** Viết script Python đánh giá tự động (Automated Evaluation) chạy qua toàn bộ 20 đề:
  - Đo tỷ lệ trích xuất đúng tham số (Mục tiêu KPI-01: $\ge 85\%$).
  - Đo sai số tính toán so với đáp án chuẩn (Mục tiêu KPI-02: $\le 2\%$).
  - Đo thời gian phản hồi hệ thống (Mục tiêu KPI-05: $\le 15s$).
  - Đo tỷ lệ trích dẫn đúng số trang giáo trình (Mục tiêu KPI-04: $\ge 80\%$).
- [ ] **T-QA-06:** Kiểm thử các trường hợp biên (Edge Cases): ảnh chụp mờ, ảnh chụp nghiêng góc $90^\circ$, câu hỏi ngoài phạm vi môn học (FR-14).

---

## 2. Kịch Bản Demo Trên Lớp & Tài Liệu Cho Sinh Viên (Phụ lục B SRS)
- [x] **T-DEMO-01:** Soạn tài liệu hướng dẫn và kịch bản demo chi tiết tại [docs/USER_GUIDE.md](file:///run/media/tamdae/Data/Source%20code/rag_agent/docs/USER_GUIDE.md).
- [ ] **T-DEMO-02:** Soạn kịch bản trình diễn 10 phút chi tiết theo từng phút (Phút 1-2: Giới thiệu; Phút 3-5: Giải bài tập ảnh 1; Phút 6-7: Giải bài tập sơ đồ 2; Phút 8-9: RAG Hỏi đáp chuyên ngành; Phút 10: Tổng kết).
- [ ] **T-DEMO-03:** Chuẩn bị bộ 10 câu hỏi phản biện "tủ" của hội đồng giảng viên kèm câu trả lời ngắn gọn, chuẩn thuật ngữ điện cho bạn sinh viên học thuộc.
- [ ] **T-DEMO-04:** Kiểm tra kịch bản dự phòng khi máy chiếu lớp học không có mạng Internet (sử dụng cơ chế Fallback/Mock có sẵn).
- [ ] **T-DEMO-05:** Buổi tập dượt thực tế (Rehearsal): bạn sinh viên tự tay bấm đúp mở file `.bat`, tải ảnh, kiểm tra tham số và trả lời thử các câu hỏi.

---

## 3. Sản Phẩm Bàn Giao & Báo Cáo 7 Chương (Mục 15.1 SRS)
- [ ] **Chương 1:** Tổng quan đề tài và bài toán đặt ra trong học phần Tự động hóa lưới điện phân phối.
- [ ] **Chương 2:** Cơ sở lý thuyết: Lưới điện phân phối, AI Agent, Mô hình đa phương thức, Cơ chế RAG từ PDF duy nhất và Vector Database.
- [ ] **Chương 3:** Phân tích yêu cầu và đặc tả hệ thống (SRS v1.2).
- [ ] **Chương 4:** Thiết kế kiến trúc tổng thể, cơ sở dữ liệu SQLite, Vector Store và thiết kế giao diện UI/UX Pro Max.
- [ ] **Chương 5:** Triển khai cài đặt hệ thống: Backend FastAPI, Multimodal Vision, Bộ tính toán an toàn Python, React Web và Electron Desktop.
- [ ] **Chương 6:** Kiểm thử và đánh giá độ chính xác trên bộ 20 đề thực tế (Kèm bảng số liệu KPI).
- [ ] **Chương 7:** Kết luận, các hạn chế và hướng phát triển mở rộng.
