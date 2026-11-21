# HƯỚNG DẪN SỬ DỤNG VÀ KỊCH BẢN DEMO ĐỒ ÁN
*(Tài liệu dành cho sinh viên không chuyên IT - Đảm bảo demo thành công 100%)*

---

## 1. Chuẩn bị trước buổi Demo (Thực hiện ở nhà)

### Bước 1: Lấy API Key miễn phí từ Google (Chỉ làm 1 lần)
1. Dùng trình duyệt mở: https://aistudio.google.com/
2. Đăng nhập bằng tài khoản Google (Gmail).
3. Bấm nút **"Get API key"** $\rightarrow$ Bấm **"Create API key"**.
4. Sao chép (Copy) đoạn mã khóa vừa tạo.
5. Mở tệp `backend/.env` (hoặc tạo từ `backend/.env.example`), dán mã khóa vào dòng:
   ```env
   GEMINI_API_KEY=dán_mã_khóa_vào_đây
   ```

### Bước 2: Chạy thử trên máy tính của bạn
- **Trên Windows:** Bấm đúp chuột vào file `scripts/run_windows.bat`.
- **Trên Linux / Mac:** Chạy lệnh `bash scripts/run_linux.sh`.
- Hệ thống sẽ tự động bật cửa sổ ứng dụng Desktop và trình duyệt web.

---

## 2. Kịch bản Demo trực tiếp trước Giảng viên (3 Phút hoàn hảo)

### Phần 1: Giới thiệu ngắn gọn (30 giây)
> *"Thưa thầy/cô, đồ án của em xây dựng AI Agent trợ lý học tập cho học phần Tự động hóa lưới điện phân phối. Điểm đặc biệt của hệ thống là:*
> 1. *Tiếp nhận đề bài bằng ảnh tiếng Trung, bóc tách sơ đồ mạch điện và công thức.*
> 2. *Tích hợp bộ tính toán an toàn Python để loại bỏ hoàn toàn sai số tính nhẩm của AI.*
> 3. *Chỉ sử dụng duy nhất một cuốn PDF giáo trình của môn học làm căn cứ, trích dẫn rõ số trang.*
> 4. *Hỗ trợ song ngữ: Giai đoạn 1 hiển thị tiếng Việt, có thể chuyển sang tiếng Trung giản thể."*

### Phần 2: Demo Chức năng 1 - Giải bài tập qua ảnh (1 phút)
1. Chọn tab **"Giải bài tập qua ảnh"**.
2. Bấm vào ô tải ảnh, chọn file mẫu: `sample-data/questions/anh_bai_tap_mau.jpeg`.
3. Bấm nút **"Bắt đầu phân tích & giải bài"**.
4. Chỉ cho thầy cô thấy kết quả trên màn hình:
   - **Mục 1:** Hệ thống đọc được nguyên văn chữ tiếng Trung và dịch diễn giải sang tiếng Việt, lập bảng thông số ($P = 1200\text{ kW}, \cos\varphi = 0.85, R = 2.5\ \Omega, X = 3.2\ \Omega$).
   - **Mục 2:** Lời giải từng bước chi tiết kèm công thức $\Delta U = \frac{P \cdot R + Q \cdot X}{U_n}$. Có huy hiệu **"Đã kiểm chứng bằng Python Calculator"**.
   - **Mục 3:** Đáp số cuối cùng $\Delta U = 538.08\text{ V}$ và trích dẫn: **"PDF giáo trình, trang 42"**.

### Phần 3: Demo Chức năng 2 - Hỏi đáp chuyên ngành (1 phút)
1. Chuyển sang tab **"Hỏi đáp chuyên ngành (PDF)"**.
2. Nhập một câu hỏi lý thuyết, ví dụ:
   > *"Dao cắt tự đóng lại (Recloser) hoạt động như thế nào trong tự động hóa lưới điện phân phối?"*
   > *(Hoặc câu tiếng Trung: 重合器的工作原理是什么？)*
3. Bấm **"Gửi"**.
4. Hệ thống sẽ trả lời cấu trúc 4 phần rõ ràng:
   - Trả lời trực tiếp định nghĩa.
   - Giải thích cơ chế cắt - đóng lại.
   - Liên hệ tự động hóa lưới điện (phối hợp Recloser với Sectionalizer).
   - Trích dẫn chính xác: **"PDF giáo trình, trang 140"**.

---

## 3. Bộ câu hỏi thường gặp khi Thầy/Cô phản biện

### Q1: "Tại sao phần mềm tính toán ra con số này, có chắc là AI không tính nhầm không?"
**Trả lời:**
> *"Dạ thưa thầy/cô, hệ thống của em không để AI tự tính nhẩm. AI chỉ làm nhiệm vụ bóc tách thông số ($P, Q, R, X, U$). Sau đó, toàn bộ số liệu được truyền vào hàm Python viết bằng công thức chuẩn kỹ thuật điện để tính toán ra đáp số chính xác 100%, rồi AI mới định dạng lại lời giải từng bước ạ."*

### Q2: "Nếu ảnh chụp đề bài bị mờ hoặc rách thì hệ thống xử lý thế nào?"
**Trả lời:**
> *"Dạ thưa thầy/cô, theo yêu cầu FR-08 trong đặc tả, khi gặp số liệu mờ, hệ thống sẽ đánh dấu `is_confirmed = False`, hiển thị cảnh báo nghi vấn và cho phép người dùng nhập sửa trực tiếp trên giao diện trước khi giải, không tự ý đoán mò số liệu ạ."*

### Q3: "Hệ thống có lấy tài liệu linh tinh trên mạng về không?"
**Trả lời:**
> *"Dạ hoàn toàn không ạ. Hệ thống bị khóa cứng (Grounded RAG) vào duy nhất file PDF giáo trình 233 trang của môn học được nạp cố định ở backend. Nếu câu hỏi nằm ngoài giáo trình, hệ thống sẽ thông báo rõ là giáo trình chưa cung cấp đủ thông tin chứ không tự lấy nguồn ngoài ạ."*
