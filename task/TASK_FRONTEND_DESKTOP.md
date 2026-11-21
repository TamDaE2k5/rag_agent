# TASK CHI TIẾT: GIAO DIỆN WEB & DESKTOP ELECTRON

Mục tiêu: Xây dựng giao diện trực quan, mượt mà, hỗ trợ song ngữ, hiển thị công thức toán học chuẩn xác, ứng dụng tri thức từ `ui-ux-pro-max-skill`.

---

## 1. Giao Diện Người Dùng Web (React + Tailwind CSS)
- [x] **T-FE-01:** Khởi tạo dự án Vite + React + TypeScript + Tailwind CSS.
- [x] **T-FE-02:** Thiết kế Navbar hiện đại với logo, chuyển tab và nút gạt song ngữ VI / zh-CN.
- [x] **T-FE-03:** Xây dựng component `ImageSolver`: vùng tải ảnh, xem trước ảnh, nút xoay ảnh $90^\circ$.
- [x] **T-FE-03B:** Bổ sung xử lý sự kiện kéo thả thực sự (`onDragOver`, `onDragLeave`, `onDrop`) thay vì chỉ click chọn file.
- [x] **T-FE-04:** Bố cục kết quả lời giải 3 phần rõ ràng:
  - Bảng dữ kiện trích xuất & sơ đồ.
  - Lời giải chi tiết từng bước có huy hiệu kiểm chứng toán học.
  - Kết luận đáp số & thẻ trích dẫn số trang giáo trình.
- [x] **T-FE-05:** Xây dựng component `ChatGrounded` cho luồng hỏi đáp chuyên ngành từ PDF giáo trình.
- [x] **T-FE-06 (HIGH):** Tích hợp render KaTeX thực tế: hiển thị công thức toán học $\LaTeX$ đẹp mắt thay vì in chuỗi thô `{step.formula_latex}`.
- [x] **T-FE-07 (FR-08):** Bổ sung Modal/Bảng cho phép người dùng click sửa trực tiếp giá trị các tham số mờ hoặc nhận diện sai trước khi bấm "Giải lại".
- [x] **T-FE-08 (FR-16):** Thêm nút "Sao chép lời giải" (Copy to Clipboard) định dạng Markdown/Text kèm toast thông báo thành công.
- [x] **T-FE-09 (FR-17):** Hiển thị thanh tiến trình xử lý chi tiết (Đang tiền xử lý ảnh $\rightarrow$ Trích xuất $\rightarrow$ Tra cứu giáo trình $\rightarrow$ Tính toán).
- [x] **T-FE-10:** Hộp thoại xem trích dẫn sách gốc (Source Excerpt Modal): bấm vào số trang để đọc đoạn văn bản gốc và bản dịch tiếng Việt.
- [x] **T-FE-11:** Hiệu ứng gõ phím / typing spinner khi gửi câu hỏi trong màn hình `ChatGrounded`.

---

## 2. Ứng Dụng Máy Tính Desktop (Electron)
- [x] **T-DT-01:** Khởi tạo cấu hình Electron trong thư mục `desktop/`.
- [x] **T-DT-02:** Viết `main.js` với cơ chế kiểm tra sức khỏe backend (`/api/health`) trước khi hiển thị cửa sổ.
- [x] **T-DT-03:** Thiết lập `preload.js` an toàn với `contextIsolation: true`.
- [ ] **T-DT-04:** Kiểm thử khởi chạy ứng dụng Electron thực tế kết nối với backend FastAPI.
- [ ] **T-DT-05:** Cấu hình Electron Builder đóng gói thành bộ cài đặt `.exe` độc lập trên Windows.
- [x] **T-DT-06:** Viết script 1-Click `run_windows.bat` và `run_linux.sh` cho phép bạn sinh viên bấm đúp chuột là tự chạy cả hệ thống.
- [ ] **T-DT-07:** Kiểm tra khả năng chạy offline hoàn toàn (sử dụng cơ chế Fallback/Mock) trong trường hợp phòng thi/hội đồng không có WiFi.
