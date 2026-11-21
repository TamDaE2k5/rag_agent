import uuid
from typing import Dict, Any, Optional
from backend.app.services.image_service import image_service
from backend.app.services.calculator_service import calculator
from backend.app.services.rag_service import rag_service
from backend.app.providers.gemini_provider import gemini_provider
from backend.app.agent.prompts import (
    SOLVER_SYSTEM_PROMPT_VI,
    SOLVER_SYSTEM_PROMPT_ZH,
    CHAT_SYSTEM_PROMPT_VI
)
from backend.app.core.logger import logger

class AgentOrchestrator:
    """
    Bộ điều phối AI Agent: kết hợp Vision, RAG từ PDF duy nhất và Calculator an toàn
    """
    
    async def solve_from_image(
        self,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        rotate_angle: int = 0,
        language: str = "vi"
    ) -> Dict[str, Any]:
        session_id = str(uuid.uuid4())
        
        # 1. Tiền xử lý ảnh (xoay, tăng tương phản)
        processed_bytes, _ = image_service.preprocess_image(
            image_bytes, rotate_angle=rotate_angle
        )
        
        # 2. Xây dựng prompt kèm ngữ cảnh
        sys_prompt = SOLVER_SYSTEM_PROMPT_VI if language == "vi" else SOLVER_SYSTEM_PROMPT_ZH
        user_prompt = (
            "Hãy đọc đề bài tiếng Trung trong ảnh, trích xuất dữ kiện, sơ đồ (nếu có) "
            "và trình bày lời giải chi tiết theo các bước chuẩn mực."
        )
        
        # 3. Gọi Gemini Vision API
        ai_result = gemini_provider.generate_with_image(
            image_bytes=processed_bytes,
            mime_type=mime_type,
            prompt=user_prompt,
            system_instruction=sys_prompt
        )
        
        if "error" in ai_result and not ai_result.get("success", True):
            return {
                "session_id": session_id,
                "status": "error",
                "message": ai_result.get("error", "Lỗi khi gọi API AI")
            }

        # 4. Tìm kiếm trang căn cứ giáo trình từ từ khóa của bài toán
        raw_text = ai_result.get("raw_text_zh", "")
        if raw_text:
            matches = rag_service.search(raw_text[:100], top_k=1)
            if matches:
                ai_result["textbook_reference"] = matches[0]["reference"]

        # 5. Hỗ trợ kiểm tra lại các phép tính bằng Python Calculator (FR-10, FR-11)
        params = {p.get("symbol"): p.get("value") for p in ai_result.get("parameters", []) if p.get("value") is not None}
        
        # Kiểm tra tính toán tổn thất điện áp nếu có đủ thông số P, Q hoặc cos_phi, R, X, U
        if "P" in params and "R" in params and "X" in params and ("U_n" in params or "U" in params):
            u_val = params.get("U_n") or params.get("U")
            q_val = params.get("Q", 0.0)
            if q_val == 0.0 and "cos_phi" in params:
                cos_p = params["cos_phi"]
                if 0 < cos_p < 1:
                    import math
                    tan_p = math.tan(math.acos(cos_p))
                    q_val = params["P"] * tan_p
            
            calc_res = calculator.calculate_voltage_drop(
                p_kw=params["P"],
                q_kvar=q_val,
                r_ohm=params["R"],
                x_ohm=params["X"],
                u_kv=u_val
            )
            if calc_res.get("success"):
                logger.info(f"Verified voltage drop with deterministic calculator: {calc_res['calculation_str']}")

        ai_result["session_id"] = session_id
        ai_result["status"] = "success"
        ai_result["language"] = language
        return ai_result

    async def answer_chat(
        self,
        question: str,
        session_id: Optional[str] = None,
        language: str = "vi"
    ) -> Dict[str, Any]:
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # 1. Truy xuất RAG từ PDF giáo trình tiếng Trung duy nhất
        grounded_context, refs = rag_service.get_grounded_context(question)
        
        # 2. Xây dựng prompt kèm ngữ cảnh tài liệu
        prompt = f"CÂU HỎI: {question}\n\n"
        if grounded_context:
            prompt += f"CÁC ĐOẠN TRÍCH TỪ PDF GIÁO TRÌNH TIẾNG TRUNG:\n{grounded_context}\n\n"
            prompt += "Hãy căn cứ vào các đoạn trích trên để trả lời đầy đủ, chính xác và trích dẫn số trang."
        else:
            prompt += "LƯU Ý: Không tìm thấy đoạn trích phù hợp trong PDF giáo trình. Hãy thông báo rõ cho người dùng."

        # 3. Gọi Gemini Chat API
        result = gemini_provider.generate_chat(
            prompt=prompt,
            system_instruction=CHAT_SYSTEM_PROMPT_VI
        )
        
        result["session_id"] = session_id
        result["language"] = language
        if refs and ("PDF" not in result.get("textbook_reference", "")):
            result["textbook_reference"] = refs[0]
            
        return result

orchestrator = AgentOrchestrator()
