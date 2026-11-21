@echo off
chcp 65001 > nul
echo =====================================================================
echo    KHỞI ĐỘNG HỆ THỐNG AI AGENT TỰ ĐỘNG HÓA LƯỚI ĐIỆN PHÂN PHỐI
echo =====================================================================
echo.

:: 1. Kiểm tra môi trường Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Chưa cài đặt Python trên máy tính! Vui lòng cài Python 3.10+
    pause
    exit /b
)

:: 2. Khởi động Backend FastAPI ngầm
echo [1/3] Đang khởi động Backend FastAPI (Port 8000)...
start "Backend - AI Agent" cmd /c "set PYTHONPATH=. && python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"

:: Đợi 3 giây để Backend sẵn sàng
timeout /t 3 /nobreak > nul

:: 3. Khởi động Frontend Web & Desktop
echo [2/3] Đang khởi động Giao diện Web (Port 5173)...
cd frontend
if not exist node_modules (
    echo Đang cài đặt thư viện frontend...
    call npm install
)
start "Frontend - Vite" cmd /c "npm run dev"

:: 4. Mở trình duyệt tự động
timeout /t 2 /nobreak > nul
echo [3/3] Đang mở ứng dụng trên trình duyệt...
start http://localhost:5173

echo.
echo =====================================================================
echo    HỆ THỐNG ĐÃ SẴN SÀNG! Bạn có thể bắt đầu sử dụng để demo.
echo =====================================================================
pause
