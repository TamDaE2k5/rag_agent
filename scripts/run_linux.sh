#!/usr/bin/env bash
set -e

echo "====================================================================="
echo "   KHỞI ĐỘNG HỆ THỐNG AI AGENT TỰ ĐỘNG HÓA LƯỚI ĐIỆN PHÂN PHỐI"
echo "====================================================================="

# 1. Khởi động backend
echo "[1/2] Đang khởi động Backend FastAPI..."
export PYTHONPATH=.
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

trap "kill $BACKEND_PID" EXIT

# 2. Khởi động frontend
echo "[2/2] Đang khởi động Frontend Web..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Đang cài đặt thư viện frontend..."
    npm install
fi

echo "Mở ứng dụng tại http://localhost:5173"
npm run dev
