# TASK CHI TIẾT: GIAO DIỆN WEB & DESKTOP ELECTRON

Mục tiêu: Xây dựng giao diện trực quan, mượt mà, hỗ trợ song ngữ, ứng dụng tri thức từ `ui-ux-pro-max-skill`.

---

## 1. Giao Diện Người Dùng Web (React + Tailwind CSS)
- [x] **T-FE-01:** Khởi tạo dự án Vite + React + TypeScript + Tailwind CSS.
- [x] **T-FE-02:** Thiết kế Navbar hiện đại với logo, chuyển tab và nút gạt song ngữ VI / zh-CN.
- [x] **T-FE-03:** Xây dựng component `ImageSolver`: vùng kéo thả ảnh, xem trước ảnh, nút xoay ảnh.
- [x] **T-FE-04:** Bố cục kết quả lời giải 3 phần rõ ràng:
  - Bảng dữ kiện trích xuất & sơ đồ.
  - Lời giải chi tiết từng bước có huy hiệu kiểm chứng toán học.
  - Kết luận đáp số & thẻ trích dẫn số trang giáo trình.
- [x] **T-FE-05:** Xây dựng component `ChatGrounded` cho luồng hỏi đáp chuyên ngành từ PDF giáo trình.
- [x] **T-FE-06:** Tích hợp KaTeX để hiển thị công thức toán học và biểu thức kỹ thuật điện ($\LaTeX$).
- [ ] **T-FE-07:** Bổ sung modal cho phép người dùng click sửa trực tiếp giá trị các tham số mờ (FR-08).
- [ ] **T-FE-08:** Thêm nút "Sao chép lời giải" (Copy to Clipboard) dạng Markdown (FR-16).

---

## 2. Ứng Dụng Máy Tính Desktop (Electron)
- [x] **T-DT-01:** Khởi tạo cấu hình Electron trong thư mục `desktop/`.
- [x] **T-DT-02:** Viết `main.js` với cơ chế kiểm tra sức khỏe backend (`/api/health`) trước khi hiển thị cửa sổ.
- [x] **T-DT-03:** Thiết lập `preload.js` an toàn với `contextIsolation: true`.
- [ ] **T-DT-04:** Cấu hình Electron Builder đóng gói thành bộ cài đặt `.exe` độc lập trên Windows.
- [x] **T-DT-05:** Viết script 1-Click `run_windows.bat` cho phép bạn sinh viên bấm đúp chuột là tự chạy cả hệ thống.
