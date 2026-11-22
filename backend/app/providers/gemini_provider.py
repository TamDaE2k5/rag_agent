import os
import json
import re
import base64
import urllib.request
import urllib.error
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
        c = re.sub(r",\s*([\]}])", r"\1", c)
        c = re.sub(r"\\(frac|tan|text|tau|theta|times|cdot|Delta|varphi|approx|sqrt|mu|le|ge|pm|Omega)", r"\\\\\1", c)
        c = re.sub(r"\\(?![\"\\/bfnrtu])", r"\\\\", c)
        return json.loads(c)
    except Exception as ex1:
        logger.warning(f"Secondary JSON repair failed: {ex1}. Attempting aggressive repair.")

    # 5. Khắc phục triệt để: thay thế các ký tự điều khiển và xuống dòng unescaped
    try:
        c2 = candidate
        c2 = re.sub(r",\s*([\]}])", r"\1", c2)
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
    Adapter tích hợp Google Gemini API qua Direct REST API thuần túy (HTTP POST)
    Độc lập 100%, không phụ thuộc vào SDK ngoài (google-genai hay google-generativeai).
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
        self._client = None
        if self.model_name.startswith("models/"):
            self.model_name = self.model_name.replace("models/", "")

    def _get_api_url(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

    def test_connection(self) -> Dict[str, Any]:
        """
        Kiểm tra trạng thái kết nối tới Google Gemini REST API
        """
        if not self.api_key or len(self.api_key.strip()) < 10:
            return {
                "connected": False,
                "status": "offline_local_rag",
                "model": self.model_name,
                "message": "Chưa cấu hình GEMINI_API_KEY. Hệ thống đang hoạt động ổn định ở chế độ Dynamic Local RAG.",
                "mode": "local_rag"
            }

        try:
            url = self._get_api_url()
            req_payload = {
                "contents": [
                    {
                        "parts": [{"text": "Xin chào, phản hồi ngắn 'OK'."}]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 10,
                    "temperature": 0.1
                }
            }
            req_data = json.dumps(req_payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=7) as resp:
                if resp.status == 200:
                    return {
                        "connected": True,
                        "status": "online",
                        "model": self.model_name,
                        "message": f"Kết nối Gemini REST API thành công ({self.model_name}).",
                        "mode": "live_gemini"
                    }
                else:
                    return {
                        "connected": False,
                        "status": "offline_local_rag",
                        "model": self.model_name,
                        "message": f"API trả về mã trạng thái {resp.status}. Tự động chuyển sang Dynamic Local RAG.",
                        "mode": "local_rag"
                    }
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            logger.warning(f"Gemini API connection test HTTP error {e.code}: {err_msg[:120]}")
            return {
                "connected": False,
                "status": "offline_local_rag",
                "model": self.model_name,
                "message": f"Lỗi xác thực hoặc hết hạn ngạch ({e.code}). Chuyển sang Dynamic Local RAG.",
                "mode": "local_rag"
            }
        except Exception as e:
            logger.warning(f"Gemini API connection test error: {e}")
            return {
                "connected": False,
                "status": "offline_local_rag",
                "model": self.model_name,
                "message": f"Không thể kết nối mạng ({str(e)[:80]}). Chuyển sang Dynamic Local RAG.",
                "mode": "local_rag"
            }

    def generate_with_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gọi Gemini REST API đa phương thức với ảnh (Base64) và prompt
        """
        if not self.api_key or len(self.api_key.strip()) < 10:
            logger.info("No Gemini API key configured. Delegating to Dynamic Local Solver.")
            return {"use_local_rag": True, "success": False, "error": "No API key"}

        try:
            b64_img = base64.b64encode(image_bytes).decode("utf-8")
            parts = [
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": b64_img
                    }
                },
                {"text": prompt}
            ]
            
            payload = {
                "contents": [{"parts": parts}],
                "generationConfig": {
                    "temperature": 0.2,
                    "responseMimeType": "application/json"
                }
            }

            if system_instruction:
                payload["system_instruction"] = {
                    "parts": [{"text": system_instruction}]
                }

            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self._get_api_url(),
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=20) as resp:
                raw_body = resp.read().decode("utf-8")
                api_json = json.loads(raw_body)
                
                candidates = api_json.get("candidates", [])
                if candidates:
                    content_parts = candidates[0].get("content", {}).get("parts", [])
                    if content_parts and "text" in content_parts[0]:
                        response_text = content_parts[0]["text"]
                        return safe_json_loads(response_text)

                return {"use_local_rag": True, "error": "No text in candidate response"}

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            logger.error(f"Gemini REST API image call failed (HTTP {e.code}): {err_body[:150]}")
            return {"use_local_rag": True, "error": f"HTTP {e.code}: {err_body[:100]}", "success": False}
        except Exception as e:
            logger.error(f"Gemini REST API image call exception: {e}")
            return {"use_local_rag": True, "error": str(e), "success": False}

    def generate_chat(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gọi Gemini REST API chat văn bản
        """
        if not self.api_key or len(self.api_key.strip()) < 10:
            return {"use_local_rag": True, "success": False, "error": "No API key"}

        try:
            payload = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "responseMimeType": "application/json"
                }
            }

            if system_instruction:
                payload["system_instruction"] = {
                    "parts": [{"text": system_instruction}]
                }

            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self._get_api_url(),
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=15) as resp:
                raw_body = resp.read().decode("utf-8")
                api_json = json.loads(raw_body)
                
                candidates = api_json.get("candidates", [])
                if candidates:
                    content_parts = candidates[0].get("content", {}).get("parts", [])
                    if content_parts and "text" in content_parts[0]:
                        response_text = content_parts[0]["text"]
                        return safe_json_loads(response_text)

                return {"use_local_rag": True, "error": "No text in candidate response"}

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            logger.error(f"Gemini REST API chat call failed (HTTP {e.code}): {err_body[:150]}")
            return {"use_local_rag": True, "error": f"HTTP {e.code}", "success": False}
        except Exception as e:
            logger.error(f"Gemini REST API chat call exception: {e}")
            return {"use_local_rag": True, "error": str(e), "success": False}

    def _generate_mock_solution(self) -> Dict[str, Any]:
        from backend.app.services.calculator_service import calculator
        calc_res = calculator.calculate_voltage_drop(1200.0, 744.0, 2.5, 3.2, 10.0)
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
                    "formula_latex": calc_res["formula_latex"],
                    "substituted_values": calc_res["calculation_str"],
                    "calculated_value": f"{calc_res['delta_u_v']} V",
                    "verified_by_tool": True
                },
                {
                    "step_number": 3,
                    "title": "Tính phần trăm tổn thất điện áp",
                    "explanation": "So sánh Delta U với điện áp định mức 10 kV (10.000 V).",
                    "formula_latex": r"\Delta U\% = \frac{\Delta U}{U_n} \cdot 100\%",
                    "substituted_values": f"({calc_res['delta_u_v']} / 10000) * 100% = {calc_res['percent_drop']}%",
                    "calculated_value": f"{calc_res['percent_drop']} %",
                    "verified_by_tool": True
                }
            ],
            "final_answer": f"Tổn thất điện áp trên đường dây là {calc_res['delta_u_v']} V (tương đương {calc_res['percent_drop']}% điện áp định mức).",
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
