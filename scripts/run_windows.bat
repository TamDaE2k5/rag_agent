@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Đưa về thư mục gốc của dự án dù click đúp ở bất kỳ đâu
cd /d "%~dp0.."

echo =====================================================================
echo    KHỞI ĐỘNG HỆ THỐNG AI AGENT TỰ ĐỘNG HÓA LƯỚI ĐIỆN PHÂN PHỐI
echo =====================================================================
echo.

:: 1. Kiểm tra môi trường Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI NGUY HIỂM] Chưa cài đặt Python hoặc chưa tích chọn "Add Python to PATH"!
    echo Vui lòng xem hướng dẫn chi tiết tại file: HUONG_DAN_CHAY_WINDOWS.md
    echo Tải Python tại: https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

:: 2. Kiểm tra môi trường Node.js / npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI NGUY HIỂM] Chưa cài đặt Node.js!
    echo Vui lòng tải và cài đặt Node.js LTS tại: https://nodejs.org/
    echo.
    pause
    exit /b
)

:: 3. Kiểm tra file cấu hình .env
if not exist "backend\.env" (
    echo [CẢNH BÁO] Chưa tìm thấy file backend\.env!
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" > nul
        echo Đã tự động tạo file backend\.env từ mẫu.
        echo LƯU Ý: Vui lòng mở file backend\.env bằng Notepad và dán GEMINI_API_KEY vào.
        echo (Xem chi tiết cách lấy Key miễn phí trong file HUONG_DAN_CHAY_WINDOWS.md)
    )
)

:: 4. Kiểm tra thư viện Backend
echo [1/4] Đang kiểm tra thư viện Python Backend...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Đang tự động cài đặt các thư viện cần thiết cho Backend...
    pip install -r backend\requirements.txt
)

:: 5. Khởi động Backend FastAPI ngầm
echo [2/4] Đang khởi động Backend FastAPI (Port 8000)...
start "Backend - AI Agent Grid" cmd /k "set PYTHONPATH=. && python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"

:: Đợi 3 giây để Backend khởi động
timeout /t 3 /nobreak > nul

:: 6. Kiểm tra & Khởi động Frontend
echo [3/4] Đang kiểm tra và khởi động Giao diện Web (Port 5173)...
cd frontend
if not exist "node_modules" (
    echo Lần đầu chạy: Đang tự động cài đặt thư viện Frontend (có thể mất 1-2 phút)...
    call npm install
)
start "Frontend - AI Agent Vite" cmd /k "npm run dev"
cd ..

:: 7. Mở trình duyệt tự động
timeout /t 3 /nobreak > nul
echo [4/4] Đang mở ứng dụng trên trình duyệt web...
start http://localhost:5173

echo.
echo =====================================================================
echo    HỆ THỐNG ĐÃ KHỞI ĐỘNG XONG!
echo    - Cửa sổ Backend và Frontend đang chạy song song.
echo    - Trình duyệt đã mở tại: http://localhost:5173
echo    - Khi muốn tắt hệ thống: Đóng các cửa sổ dòng lệnh đen là xong.
echo =====================================================================
echo.
pause
