# HƯỚNG DẪN CÀI ĐẶT & CHẠY DỰ ÁN TRÊN WINDOWS (TỪ SỐ 0)
> **Dành riêng cho sinh viên ngành Điện:** Tài liệu này được viết từng bước cực kỳ chi tiết, dễ hiểu, không yêu cầu kiến thức về lập trình hay công nghệ thông tin. Máy tính Windows mới tinh chưa cài gì cũng làm được trong 5-10 phút.

---

## 📑 TỔNG QUAN CÁC BƯỚC THỰC HIỆN
1. **Bước 1:** Lấy mã khóa Google Gemini API miễn phí (2 phút).
2. **Bước 2:** Cài đặt Python (2 phút - *chú ý 1 nút bấm quan trọng*).
3. **Bước 3:** Cài đặt Node.js (2 phút - chỉ cần bấm Next).
4. **Bước 4:** Tải mã nguồn dự án về máy.
5. **Bước 5:** Điền mã khóa API vào tệp cấu hình.
6. **Bước 6:** Bấm đúp chuột để chạy hệ thống (1-Click).

---

## BƯỚC 1: LẤY MÃ KHÓA GOOGLE GEMINI API (HOÀN TOÀN MIỄN PHÍ)
*Mã khóa API giống như "chìa khóa" để phần mềm gửi ảnh đề bài tiếng Trung cho trí tuệ nhân tạo của Google đọc và giải.*

1. Mở trình duyệt web (Chrome, Edge hoặc Cốc Cốc) và truy cập đường link:  
   👉 **https://aistudio.google.com/app/apikey**
2. Đăng nhập bằng tài khoản **Gmail** thông thường của bạn.
3. Nếu Google hỏi điều khoản sử dụng, bạn tích chọn **"I agree"** và bấm **"Continue"**.
4. Bạn nhìn thấy nút màu xanh có chữ **"Create API key"** (hoặc **"Get API key"**):
   - Bấm vào nút **"Create API key"**.
   - Chọn mục **"Create API key in new project"** (Tạo khóa trong dự án mới).
5. Một dòng mã khóa dài xuất hiện (thường bắt đầu bằng chữ `AIzaSy...`):
   - Bấm nút **Copy** để sao chép mã khóa này.
   - Dán tạm mã khóa vào Zalo hoặc Notepad để tí nữa dùng ở Bước 5.

> 💡 **Lưu ý:** Gói miễn phí này của Google hoàn toàn không mất tiền, không cần thẻ tín dụng ngân hàng.

---

## BƯỚC 2: CÀI ĐẶT PYTHON TRÊN MÁY TÍNH
*Python là môi trường để chạy bộ máy tính toán kỹ thuật điện và cơ sở dữ liệu.*

1. Truy cập trang chủ Python:  
   👉 **https://www.python.org/downloads/**
2. Bấm vào nút màu vàng to: **"Download Python 3.12.x"** (hoặc bản 3.10, 3.11, 3.13 đều được).
3. Sau khi tải xong file `.exe`, bạn **bấm đúp chuột để mở file cài đặt**.
4. ⚠️ **BƯỚC QUAN TRỌNG NHẤT (99% NGƯỜI DÙNG QUÊN BƯỚC NÀY):**
   - Ở màn hình đầu tiên hiện ra, nhìn xuống dưới cùng, có ô vuông ghi:  
     ☑️ **"Add python.exe to PATH"** (hoặc *"Add Python to PATH"*).
   - **BẠN BẮT BUỘC PHẢI TÍCH CHỌN VÀO Ô NÀY!** (Nếu không tích, máy sẽ báo lỗi không tìm thấy Python).
5. Sau khi đã tích chọn ô trên, bấm nút **"Install Now"** ở phía trên.
6. Chờ thanh cài đặt chạy xong, nếu thấy có dòng chữ *"Disable path length limit"*, bấm vào nó một cái rồi bấm **"Close"** để hoàn tất.

---

## BƯỚC 3: CÀI ĐẶT NODE.JS TRÊN MÁY TÍNH
*Node.js là môi trường để chạy giao diện trang web.*

1. Truy cập trang chủ Node.js:  
   👉 **https://nodejs.org/**
2. Bạn sẽ thấy 2 nút tải về:
   - Hãy bấm vào nút bên trái: **"LTS - Recommended for Most Users"** (Bản ổn định nhất).
3. Tải xong file cài đặt `.msi`, bạn **bấm đúp chuột để mở**.
4. Quá trình cài đặt cực kỳ đơn giản:
   - Cứ bấm **Next** $\rightarrow$ Tích chọn *"I accept the terms..."* $\rightarrow$ Bấm **Next** liên tục $\rightarrow$ Bấm **Install**.
   - Khi bảng báo hỏi quyền Administrator hiện lên, chọn **Yes**.
   - Bấm **Finish** khi hoàn tất.

---

## BƯỚC 4: TẢI MÃ NGUỒN DỰ ÁN VỀ MÁY
Có 2 cách đơn giản để lấy code dự án về:

### Cách A: Tải file nén ZIP (Đơn giản nhất, không cần cài Git)
1. Mở link GitHub dự án:  
   👉 **https://github.com/TamDaE2k5/rag_agent**
2. Bấm vào nút màu xanh lá cây có chữ **"<> Code"**.
3. Chọn dòng dưới cùng: **"Download ZIP"**.
4. Tải xong, bạn nhấp chuột phải vào file ZIP vừa tải về $\rightarrow$ Chọn **"Extract All..."** (Giải nén) ra một ổ đĩa (ví dụ: ổ `D:\rag_agent` hoặc màn hình `Desktop`).

### Cách B: Dùng Git (Nếu máy đã có Git)
Mở cửa sổ dòng lệnh (CMD hoặc PowerShell) và gõ:
```bash
git clone https://github.com/TamDaE2k5/rag_agent.git
cd rag_agent
```

---

## BƯỚC 5: ĐIỀN MÃ KHÓA GEMINI API VÀO HỆ THỐNG

1. Mở thư mục dự án vừa giải nén ra.
2. Vào thư mục con có tên là: `backend`
3. Tìm xem có file nào tên là `.env` chưa:
   - Nếu **đã có** file `.env`: Nhấp chuột phải vào file `.env` $\rightarrow$ Chọn **Open with** $\rightarrow$ Chọn **Notepad**.
   - Nếu **chưa có**: Bạn tìm file tên là `.env.example`, nhấp chuột phải đổi tên nó thành `.env` (bỏ chữ `.example` đi), rồi mở bằng **Notepad**.
4. Bạn sẽ thấy dòng đầu tiên có nội dung:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
5. Bạn xóa chữ `your_gemini_api_key_here` đi và **dán mã khóa API** (đã lấy ở Bước 1) vào:
   ```env
   GEMINI_API_KEY=AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
6. Bấm phím **Ctrl + S** (hoặc vào File $\rightarrow$ Save) để lưu lại, sau đó đóng Notepad.

---

## BƯỚC 6: BẤM ĐÚP CHUỘT ĐỂ CHẠY (1-CLICK RUN)

1. Quay trở lại thư mục chính của dự án.
2. Mở thư mục con có tên là: `scripts`
3. Bạn sẽ nhìn thấy một file tên là: **`run_windows.bat`** (có biểu tượng 2 bánh răng cưa).
4. **Bấm đúp chuột (Double click) vào file `run_windows.bat`**.

### Điều gì sẽ xảy ra?
- File script thông minh sẽ tự động:
  1. Kiểm tra Python và Node.js.
  2. Tự động tải và cài đặt toàn bộ thư viện cần thiết (ở lần đầu tiên chạy, có thể mất 1-2 phút).
  3. Khởi động máy chủ xử lý AI (Backend).
  4. Khởi động giao diện website (Frontend).
  5. Tự động bật trình duyệt web lên và mở sẵn địa chỉ: **http://localhost:5173**.
- **Bạn chỉ việc bắt đầu sử dụng để giải bài tập hoặc demo báo cáo trước hội đồng!**

---

## ❓ CÁC CÂU HỎI & LỖI THƯỜNG GẶP (TROUBLESHOOTING)

### 1. Bấm đúp vào `run_windows.bat` thì báo lỗi *"Chưa cài đặt Python hoặc chưa tích chọn Add Python to PATH"*?
- **Nguyên nhân:** Khi cài Python ở Bước 2, bạn đã quên không tích vào ô vuông `Add python.exe to PATH`.
- **Cách sửa:** Chạy lại file cài đặt Python, chọn mục **"Modify"** hoặc gỡ ra cài lại, nhớ tích chọn ô `Add python.exe to PATH`.

### 2. Tường lửa Windows (Windows Firewall) hiện thông báo màu vàng/xanh hỏi quyền truy cập?
- **Cách xử lý:** Bấm nút **"Allow access"** (Cho phép truy cập) để hệ thống kết nối giữa giao diện và bộ xử lý.

### 3. Nếu phòng thi / phòng bảo vệ không có mạng Internet hoặc WiFi chập chờn thì sao?
- **Hệ thống có chế độ cứu cánh (Offline Fallback):** Hệ thống đã được lập trình sẵn cơ chế tự động chuyển sang chế độ mẫu dữ liệu cục bộ chuẩn. Ngay cả khi mất mạng, khi bạn tải ảnh mẫu lên, hệ thống vẫn hiển thị đầy đủ các bước giải toán, kiểm chứng công thức và trích dẫn số trang giáo trình bình thường, không bao giờ bị báo lỗi crash trước mặt giảng viên.

### 4. Muốn tắt hệ thống khi dùng xong thì làm thế nào?
- Chỉ cần đóng (bấm dấu `X`) ở các cửa sổ dòng lệnh màu đen đang chạy là toàn bộ hệ thống sẽ dừng an toàn.
