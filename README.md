# AI Agent - Công nghệ Tự động hóa Lưới điện Phân phối (Distribution Grid Automation)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Electron](https://img.shields.io/badge/Desktop-Electron-47848F?logo=electron&logoColor=white)](https://www.electronjs.org/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%20Vision-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Đồ án môn học / tốt nghiệp:** Xây dựng hệ thống AI Agent làm trợ lý học tập chuyên ngành Tự động hóa lưới điện phân phối.
> 
> Hệ thống có khả năng nhận diện ảnh đề bài bằng **tiếng Trung**, tra cứu tri thức trực tiếp từ **duy nhất một cuốn PDF giáo trình tiếng Trung (233 trang)**, kết hợp **bộ tính toán an toàn Python (Calculator)** và trình bày lời giải chi tiết bằng **tiếng Việt (Giai đoạn 1)** cùng **tiếng Trung giản thể (Giai đoạn 2)**.
>
> 🚀 **Dành cho bạn sinh viên không chuyên IT:** Xem ngay hướng dẫn cài đặt từ con số 0 trên máy tính Windows mới tại: 👉 [HUONG_DAN_CHAY_WINDOWS.md](HUONG_DAN_CHAY_WINDOWS.md) (kèm cách lấy Gemini API Key miễn phí).

---

## 📌 Các Tính Năng Nổi Bật (Khớp 100% Đặc tả SRS v1.2)

1. **Giải bài tập qua ảnh (Multimodal Vision Solver - FR-01 $\rightarrow$ FR-11):**
   - Đọc và phân tích ảnh bài tập (JPG/PNG), sơ đồ đơn tuyến lưới điện, mạch rơ-le, công thức viết tay tiếng Trung.
   - Bóc tách dữ kiện: Ký hiệu ($U_n, P, Q, R, X, \cos\varphi...$), đơn vị đo và đại lượng cần tìm.
   - Cơ chế xác nhận: Cho phép người dùng kiểm tra và sửa lại thông số nếu ảnh bị mờ trước khi tính toán.
2. **Bộ công cụ tính toán an toàn (Deterministic Calculator - FR-10, FR-11):**
   - Tích hợp hàm toán học Python độc lập, ngăn chặn hoàn toàn sai số và hiện tượng "ảo giác" (hallucination) của mô hình ngôn ngữ lớn.
   - Tự động kiểm chứng: Tổn thất điện áp $\Delta U$, trào lưu công suất, dòng ngắn mạch $I_{sc}^{(3)}$, bù công suất phản kháng $Q_c$.
3. **Grounded RAG từ duy nhất một PDF giáo trình tiếng Trung (FR-14, FR-23):**
   - Đóng gói sẵn cuốn giáo trình: `配电网自动化技术[郭谋发主编]2012年(OCR).pdf` (233 trang).
   - Truy xuất trực tiếp tiếng Trung, mọi câu trả lời đều trích dẫn chính xác số trang tham chiếu: `(PDF giáo trình, trang N)`.
   - Tuyệt đối không lấy dữ liệu ngoài hoặc bịa đặt trích dẫn.
4. **Hỗ trợ Song ngữ 2 giai đoạn (FR-22):**
   - **Giai đoạn 1:** Giao diện và câu trả lời hoàn toàn bằng tiếng Việt để dễ dàng kiểm thử và báo cáo.
   - **Giai đoạn 2:** Bổ sung nút chuyển đổi sang tiếng Trung giản thể (`zh-CN`).
5. **Đồng nhất Đa nền tảng (Web + Desktop Electron - FR-19):**
   - Cùng sử dụng chung Backend FastAPI, cơ sở dữ liệu SQLite và bộ chỉ mục RAG.

---

## 📂 Cấu trúc Thư mục Dự án (Theo Phụ lục A SRS)

```
rag_agent/
├── backend/
│   ├── app/
│   │   ├── main.py                 # Khởi tạo FastAPI & CORS
│   │   ├── api/v1/                 # Endpoints: solver, chat, history, settings
│   │   ├── agent/                  # Orchestrator điều phối, Prompts, Schemas
│   │   ├── services/               # ImageService, CalculatorService, RAGService
│   │   ├── providers/              # Adapter Google Gemini Vision API
│   │   ├── models/                 # SQLite database & Pydantic models
│   │   ├── core/                   # Cấu hình config (.env) & Logger
│   │   └── tests/                  # Unit tests kiểm tra tính toán điện
│   ├── knowledge/
│   │   ├── course_textbook.pdf     # PDF giáo trình tiếng Trung duy nhất (233 tr.)
│   │   └── index/                  # Chỉ mục JSON lưu text theo từng trang
│   ├── scripts/
│   │   └── ingest_pdf.py           # Script tự động trích xuất & lập chỉ mục PDF
│   ├── .env.example                # File mẫu biến môi trường
│   └── requirements.txt            # Thư viện Python cần thiết
├── frontend/
│   ├── src/
│   │   ├── components/             # Navbar, ImageSolver, ChatGrounded, HistoryList
│   │   ├── services/               # api.ts (Axios REST client)
│   │   ├── locales/                # vi.json (Giai đoạn 1) & zh-CN.json (Giai đoạn 2)
│   │   └── types/                  # TypeScript Interfaces
│   ├── package.json                # React + Tailwind + Vite
│   └── vite.config.ts
├── desktop/
│   ├── electron/
│   │   ├── main.js                 # Electron main window & backend health check
│   │   └── preload.js
│   └── package.json
├── sample-data/
│   ├── questions/                  # Ảnh đề bài mẫu (anh_bai_tap_mau.jpeg)
│   ├── answer-key/                 # Đáp án chuẩn đối chiếu
│   └── test_suite.json             # Bộ kịch bản kiểm thử mẫu (KPI-03)
├── docs/
│   ├── API.md                      # Đặc tả kỹ thuật các endpoint REST
│   ├── ARCHITECTURE.md             # Sơ đồ và nguyên lý kiến trúc logic
│   └── USER_GUIDE.md               # Hướng dẫn chi tiết & kịch bản demo cho sinh viên
├── scripts/
│   ├── run_windows.bat             # 1-Click khởi động toàn hệ thống trên Windows
│   └── run_linux.sh                # Script khởi động trên Linux / MacOS
├── .agents/skills/ui-ux-pro-max/   # Kỹ năng thiết kế UI/UX Pro Max
├── .gitignore
└── README.md
```

---

## 🚀 Hướng Dẫn Cài Đặt & Khởi Động Nhanh

### 1. Chuẩn bị Môi trường
- **Python:** Phiên bản 3.10 trở lên.
- **Node.js:** Phiên bản 18 trở lên.
- **API Key:** Lấy API key miễn phí tại [Google AI Studio](https://aistudio.google.com/).

### 2. Cấu hình Khóa API
Sao chép file cấu hình mẫu và điền API key:
```bash
cp backend/.env.example backend/.env
# Mở file backend/.env và điền GEMINI_API_KEY=...
```

### 3. Cài đặt Thư viện
```bash
# Cài đặt thư viện Backend
pip install -r backend/requirements.txt

# Cài đặt thư viện Frontend
cd frontend && npm install && cd ..
```

### 4. Khởi động 1-Click
- **Trên Windows:** Bấm đúp chuột vào file `scripts/run_windows.bat`.
- **Trên Linux / Mac:**
```bash
chmod +x scripts/run_linux.sh
./scripts/run_linux.sh
```
Trình duyệt sẽ tự động mở tại địa chỉ: `http://localhost:5173`.

---

## 🧪 Kiểm thử Đơn vị (Unit Tests)

Chạy kiểm tra bộ công cụ tính toán điện kỹ thuật:
```bash
PYTHONPATH=. python3 backend/app/tests/test_calculator.py
```
Kết quả kiểm tra:
```
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

---

## 📖 Tài Liệu Tham Khảo Thêm
- [Hướng dẫn sử dụng & Kịch bản Demo chi tiết](docs/USER_GUIDE.md)
- [Đặc tả chi tiết REST API](docs/API.md)
- [Kiến trúc hệ thống](docs/ARCHITECTURE.md)
