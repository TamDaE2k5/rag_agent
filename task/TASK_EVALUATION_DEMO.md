# TASK CHI TIẾT: KIỂM THỬ, BỘ ĐỀ MẪU & BẢO VỆ ĐỒ ÁN

Mục tiêu: Đạt chỉ số chất lượng KPI-01 $\rightarrow$ KPI-08, chuẩn bị kịch bản demo và tài liệu bàn giao để sinh viên đạt điểm tuyệt đối.

---

## 1. Bộ Dữ Liệu Kiểm Thử Chuẩn (Test Suite - KPI-03)
- [x] **T-QA-01:** Tạo thư mục `sample-data/questions/` và `sample-data/answer-key/`.
- [x] **T-QA-02:** Đưa ảnh bài tập mẫu tiếng Trung thực tế (`anh_bai_tap_mau.jpeg`) vào bộ đề test.
- [x] **T-QA-03:** Xây dựng file mô tả kịch bản test `test_suite.json` (bài tính toán tổn thất điện áp, bài phối hợp Recloser/Sectionalizer, bài tính dòng ngắn mạch).
- [ ] **T-QA-04:** Thu thập thêm 10–15 đề bài tập mẫu từ giáo trình tiếng Trung có đáp án đối chiếu để đạt chỉ tiêu 20 đề nghiệm thu (KPI-03).
- [ ] **T-QA-05:** Lập bảng đo đạc tỷ lệ chính xác (Accuracy Matrix): tỷ lệ đọc đúng ảnh, tỷ lệ truy xuất đúng trang giáo trình, tỷ lệ tính toán chính xác.

---

## 2. Kịch Bản Demo Trên Lớp (Phụ lục B SRS)
- [x] **T-DEMO-01:** Soạn tài liệu hướng dẫn và kịch bản demo chi tiết tại [docs/USER_GUIDE.md](file:///run/media/tamdae/Data/Source%20code/rag_agent/docs/USER_GUIDE.md).
- [x] **T-DEMO-02:** Chuẩn bị sẵn bộ câu hỏi phản biện thường gặp của giảng viên kèm lời giải thích chuẩn kỹ thuật điện.
- [ ] **T-DEMO-03:** Kiểm tra kịch bản dự phòng khi máy chiếu lớp học không có mạng Internet (sử dụng cơ chế Fallback/Mock có sẵn).
- [ ] **T-DEMO-04:** Tập dượt thao tác thực tế với bạn sinh viên: tải ảnh $\rightarrow$ xem thông số $\rightarrow$ kiểm tra trang sách giáo trình.

---

## 3. Sản Phẩm Bàn Giao & Báo Cáo 7 Chương (Mục 15.1 SRS)
- [ ] **Chương 1:** Tổng quan đề tài và bài toán đặt ra trong học phần Tự động hóa lưới điện phân phối.
- [ ] **Chương 2:** Cơ sở lý thuyết: Lưới điện phân phối, AI Agent, Mô hình đa phương thức, Cơ chế RAG từ PDF duy nhất và Vector Database.
- [ ] **Chương 3:** Phân tích yêu cầu và đặc tả hệ thống (SRS).
- [ ] **Chương 4:** Thiết kế kiến trúc tổng thể, cơ sở dữ liệu SQLite, Vector Store và thiết kế giao diện UI/UX.
- [ ] **Chương 5:** Triển khai cài đặt hệ thống: Backend FastAPI, Multimodal Vision, Bộ tính toán an toàn Python, React Web và Electron Desktop.
- [ ] **Chương 6:** Kiểm thử và đánh giá độ chính xác trên bộ đề thực tế.
- [ ] **Chương 7:** Kết luận, các hạn chế và hướng phát triển mở rộng.
