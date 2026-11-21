import os
import json
import re
from typing import Dict, Any, Optional, List
from backend.app.core.config import settings
from backend.app.core.logger import logger

def safe_json_loads(text: str) -> Dict[str, Any]:
    r"""
    Bộ phân tích JSON an toàn chống crash cho kết quả LLM (FR-23):
    1. Trích xuất khối mã ```json ... ``` hoặc ``` ... ``` bằng regex.
    2. Cắt bỏ các ký tự ngoài lề, tìm cặp ngoặc { ... } hoặc [ ... ].
    3. Tự động khắc phục lỗi cú pháp phổ biến của LLM:
       - Trailing commas: {"a": 1,} -> {"a": 1}
       - Unescaped LaTeX backslashes (\Delta, \frac, \times, \cdot...)
       - Ký tự xuống dòng chưa escape trong chuỗi
    4. Trả về cấu trúc Dict chuẩn, không bao giờ raise JSONDecodeError làm crash ứng dụng.
    """
    if not isinstance(text, str):
        return text if isinstance(text, dict) else {"error": "Invalid input type", "raw": str(text)}

    raw = text.strip()
    if not raw:
        return {"error": "Empty response from AI", "success": False}

    # 1. Trích xuất khối markdown code block nếu có
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw, re.IGNORECASE)
    candidate = match.group(1).strip() if match else raw

    # 2. Định vị cấu trúc JSON outermost
    if not candidate.startswith(("{", "[")):
        s_obj = candidate.find("{")
        s_arr = candidate.find("[")
        if s_obj != -1 and (s_arr == -1 or s_obj < s_arr):
            e_obj = candidate.rfind("}")
            if e_obj != -1:
                candidate = candidate[s_obj:e_obj + 1]
        elif s_arr != -1:
            e_arr = candidate.rfind("]")
            if e_arr != -1:
                candidate = candidate[s_arr:e_arr + 1]

    # 3. Thử parse trực tiếp
    try:
        return json.loads(candidate)
    except Exception:
        pass

    # 4. Áp dụng các quy tắc khử lỗi cú pháp LLM
    try:
        c = candidate
        # Khử trailing comma trước } hoặc ]
        c = re.sub(r",\s*([\]}])", r"\1", c)
        # Sửa các lệnh LaTeX phổ biến bị unescaped
        c = re.sub(r"\\(frac|tan|text|tau|theta|times|cdot|Delta|varphi|approx|sqrt|mu|le|ge|pm|Omega)", r"\\\\\1", c)
        # Escape các dấu gạch chéo ngược không hợp lệ trong chuỗi JSON
        c = re.sub(r"\\(?![\"\\/bfnrtu])", r"\\\\", c)
        
        return json.loads(c)
    except Exception as ex1:
        logger.warning(f"Secondary JSON repair failed: {ex1}. Attempting aggressive repair.")

    # 5. Khắc phục triệt để: thay thế các ký tự điều khiển và xuống dòng unescaped
    try:
        c2 = candidate
        c2 = re.sub(r",\s*([\]}])", r"\1", c2)
        # Chuyển đổi mọi backslash thành double backslash nếu chưa được escape
        c2 = re.sub(r"\\+", r"\\\\", c2)
        return json.loads(c2)
    except Exception as ex2:
        logger.error(f"Safe JSON parser failed to parse model output: {ex2}")
        return {
            "error": f"JSONDecodeError: {str(ex2)}",
            "success": False,
            "raw_text": raw[:1000]
        }

class GeminiProvider:
    """
    Adapter tích hợp Google Gemini API hỗ trợ đa phương thức (Vision + Text)
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set. GeminiProvider will operate in demo/fallback mode.")
            return

        try:
            # Ưu tiên google-genai SDK mới
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info("Initialized Google GenAI client successfully.")
        except Exception as e:
            try:
                # Fallback sang google.generativeai
                import google.generativeai as gai
                gai.configure(api_key=self.api_key)
                self._client = gai.GenerativeModel(self.model_name)
                logger.info("Initialized google.generativeai client successfully.")
            except Exception as ex:
                logger.error(f"Failed to initialize Gemini client: {ex}")
                self._client = None

    def generate_with_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gọi mô hình Vision với ảnh và prompt an toàn (FR-01, FR-02)"""
        if not self._client:
            logger.info("Gemini client not initialized or offline. Using structured mock solution.")
            return self._generate_mock_solution()

        try:
            from google import genai
            from google.genai import types
            
            contents = [
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt
            ]
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json"
            )
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            return safe_json_loads(response.text)
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Falling back to mock solution.")
            mock_res = self._generate_mock_solution()
            mock_res["warnings"] = [f"Live API fallback (lỗi: {str(e)[:120]})"]
            return mock_res

    def generate_chat(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gọi mô hình Chat văn bản có trích dẫn tài liệu với safe JSON parser (FR-12, FR-14)"""
        if not self._client:
            return self._generate_mock_chat()

        try:
            from google import genai
            from google.genai import types
            
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                response_mime_type="application/json"
            )
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            return safe_json_loads(response.text)
        except Exception as e:
            logger.error(f"Gemini chat failed: {e}. Returning mock chat response.")
            mock_chat = self._generate_mock_chat()
            mock_chat["notes"] = f"Phản hồi dự phòng (API error: {str(e)[:120]})"
            return mock_chat

    def _generate_mock_solution(self) -> Dict[str, Any]:
        return {
            "problem_type": "calculation",
            "raw_text_zh": "某10kV配电网线路，负荷P = 1200 kW, cos phi = 0.85 (感性), 线路阻抗 R = 2.5 Ohm, X = 3.2 Ohm. 试计算该线路上的电压降 Delta U 及百分比损失。",
            "interpreted_text_vi": "Đường dây phân phối 10kV cấp điện cho phụ tải có công suất P = 1200 kW, cos phi = 0.85 (tính cảm), tổng trở đường dây R = 2.5 Ohm, X = 3.2 Ohm. Tính tổn thất điện áp Delta U và tổn thất phần trăm trên đường dây.",
            "parameters": [
                {"name": "Điện áp định mức", "symbol": "U_n", "value": 10.0, "unit": "kV", "is_confirmed": True, "note": None},
                {"name": "Công suất tác dụng", "symbol": "P", "value": 1200.0, "unit": "kW", "is_confirmed": True, "note": None},
                {"name": "Hệ số công suất", "symbol": "cos_phi", "value": 0.85, "unit": "", "is_confirmed": True, "note": None},
                {"name": "Điện trở đường dây", "symbol": "R", "value": 2.5, "unit": "Ohm", "is_confirmed": True, "note": None},
                {"name": "Điện kháng đường dây", "symbol": "X", "value": 3.2, "unit": "Ohm", "is_confirmed": True, "note": None}
            ],
            "unknowns": [
                {"symbol": "Delta U", "name": "Tổn thất điện áp", "unit": "V"},
                {"symbol": "Delta U %", "name": "Phần trăm tổn thất điện áp", "unit": "%"}
            ],
            "confidence_score": 0.95,
            "requires_user_confirmation": False,
            "assumptions": ["Lưới điện 3 pha đối xứng vận hành bình thường"],
            "steps": [
                {
                    "step_number": 1,
                    "title": "Tính công suất phản kháng của phụ tải",
                    "explanation": "Từ công suất tác dụng P và hệ số công suất cos phi = 0.85, ta có tan phi = sqrt(1 - 0.85^2) / 0.85 = 0.62. Suy ra Q = P * tan phi.",
                    "formula_latex": r"Q = P \cdot \tan \varphi = 1200 \cdot 0.62",
                    "substituted_values": "1200 * 0.62 = 744.0 kvar",
                    "calculated_value": "744.0 kvar",
                    "verified_by_tool": True
                },
                {
                    "step_number": 2,
                    "title": "Tính tổn thất điện áp theo công thức",
                    "explanation": "Tổn thất điện áp trên đường dây phân phối 3 pha tính theo công thức chuẩn kỹ thuật điện.",
                    "formula_latex": r"\Delta U = \frac{P \cdot R + Q \cdot X}{U_n}",
                    "substituted_values": "(1200 * 2.5 + 744.0 * 3.2) / 10 = 538.08 V",
                    "calculated_value": "538.08 V",
                    "verified_by_tool": True
                },
                {
                    "step_number": 3,
                    "title": "Tính phần trăm tổn thất điện áp",
                    "explanation": "So sánh Delta U với điện áp định mức 10 kV (10.000 V).",
                    "formula_latex": r"\Delta U\% = \frac{\Delta U}{U_n} \cdot 100\%",
                    "substituted_values": "(538.08 / 10000) * 100% = 5.38%",
                    "calculated_value": "5.38 %",
                    "verified_by_tool": True
                }
            ],
            "final_answer": "Tổn thất điện áp trên đường dây là 538.08 V (tương đương 5.38% điện áp định mức).",
            "unit": "V",
            "textbook_reference": "PDF giáo trình, trang 42",
            "warnings": []
        }

    def _generate_mock_chat(self) -> Dict[str, Any]:
        return {
            "direct_answer": "Dao cắt tự đóng lại (Recloser - 重合器) là thiết bị đóng cắt thông minh tự động cắt và đóng lặp lại theo chu trình cài đặt sẵn khi xảy ra sự cố trên lưới điện phân phối.",
            "explanation": "Recloser có khả năng phân biệt sự cố thoáng qua (như cành cây quẹt, sét đánh) và sự cố vĩnh cửu. Nếu sự cố thoáng qua biến mất sau lần cắt đầu tiên, nó sẽ tự đóng lại thành công, khôi phục cấp điện tức thì mà không cần nhân viên vận hành đến hiện trường.",
            "course_relation": "Trong tự động hóa lưới điện phân phối (配电网自动化), Recloser thường phối hợp với Dao phân đoạn (Sectionalizer) và hệ thống FTU/SCADA để thực hiện tự động cô lập điểm sự cố và tái lập cấp điện phân đoạn (FLISR).",
            "example": "Khi sét đánh làm phóng điện sứ trên xuất tuyến 22kV, Recloser mở trong 0.5s rồi đóng lại; dòng điện phục hồi bình thường, giảm chỉ số SAIDI của lưới.",
            "textbook_reference": "PDF giáo trình, trang 140",
            "notes": "Cần lưu ý kiểm tra đường đặc tính thời gian - dòng điện (TCC) khi phối hợp bảo vệ với cầu chì hạ lưu."
        }

gemini_provider = GeminiProvider()
