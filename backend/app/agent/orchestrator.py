import uuid
import json
import math
import re
from typing import Dict, Any, Optional, List
from backend.app.services.image_service import image_service
from backend.app.services.calculator_service import calculator
from backend.app.services.rag_service import rag_service
from backend.app.providers.gemini_provider import gemini_provider
from backend.app.models.database import save_or_update_session, get_session_by_id
from backend.app.agent.prompts import (
    SOLVER_SYSTEM_PROMPT_VI,
    SOLVER_SYSTEM_PROMPT_ZH,
    CHAT_SYSTEM_PROMPT_VI
)
from backend.app.core.logger import logger

class AgentOrchestrator:
    """
    Bộ điều phối AI Agent: kết hợp Vision, RAG từ PDF duy nhất và Calculator an toàn
    Triển khai toàn diện Agent Loop: Confidence Check -> RAG Grounding -> Deterministic Verification -> Auto-Correction
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
        
        # 2. Xây dựng prompt kèm chỉ dẫn hệ thống
        sys_prompt = SOLVER_SYSTEM_PROMPT_VI if language == "vi" else SOLVER_SYSTEM_PROMPT_ZH
        user_prompt = (
            "Hãy đọc đề bài tiếng Trung trong ảnh, trích xuất dữ kiện, sơ đồ (nếu có) "
            "và trình bày lời giải chi tiết theo các bước chuẩn mực kỹ thuật điện phân phối."
        )
        
        # 3. Bước 1: Vision Extraction
        ai_result = gemini_provider.generate_with_image(
            image_bytes=processed_bytes,
            mime_type=mime_type,
            prompt=user_prompt,
            system_instruction=sys_prompt
        )
        
        if "error" in ai_result and not ai_result.get("success", True) and "problem_type" not in ai_result:
            return {
                "session_id": session_id,
                "status": "error",
                "message": ai_result.get("error", "Lỗi khi gọi API AI")
            }

        # 4. Bước 2: Confidence Check (FR-08)
        parameters = ai_result.get("parameters", [])
        confidence_score = float(ai_result.get("confidence_score", 0.95))
        requires_user_confirmation = bool(ai_result.get("requires_user_confirmation", False))
        warnings = list(ai_result.get("warnings", []))

        # Kiểm tra từng tham số: nếu có tham số bị mờ, không chắc chắn hoặc ghi chú nghi vấn
        has_uncertain_param = False
        for p in parameters:
            if p.get("is_confirmed") is False:
                has_uncertain_param = True
            note = str(p.get("note") or "").lower()
            if any(w in note for w in ["mờ", "nghi vấn", "không rõ", "unclear", "blur"]):
                p["is_confirmed"] = False
                has_uncertain_param = True

        if has_uncertain_param or confidence_score < 0.85:
            requires_user_confirmation = True
            status = "requires_confirmation"
            warnings.append("Một số thông số đề bài bị mờ hoặc chưa được xác nhận hoàn toàn. Vui lòng kiểm tra lại trước khi tiếp tục.")
        else:
            status = "success"

        # 5. Bước 3: RAG Retrieval - Tìm kiếm cơ sở lý thuyết từ PDF giáo trình duy nhất (FR-14, FR-23)
        raw_text = ai_result.get("raw_text_zh", "")
        textbook_ref = ai_result.get("textbook_reference", "PDF giáo trình, trang --")
        search_query = raw_text[:120] if raw_text else ai_result.get("interpreted_text_vi", "")[:120]
        if search_query:
            rag_matches = rag_service.search(search_query, top_k=2)
            if rag_matches:
                top_match = rag_matches[0]
                textbook_ref = top_match["reference"]
                logger.info(f"RAG Grounded textbook reference: {textbook_ref} (Score: {top_match.get('score', 0):.2f})")

        # 6. Bước 4 & Bước 5: Deterministic Calculator Verification & Auto-Correction (FR-10, FR-11)
        param_dict = {
            p.get("symbol"): p.get("value")
            for p in parameters
            if p.get("value") is not None
        }
        steps = ai_result.get("steps", [])

        # Trường hợp 1: Tính toán tổn thất điện áp Delta U
        if "P" in param_dict and "R" in param_dict and "X" in param_dict and ("U_n" in param_dict or "U" in param_dict):
            u_val = param_dict.get("U_n") or param_dict.get("U")
            q_val = param_dict.get("Q", 0.0)
            if (q_val == 0.0 or q_val is None) and "cos_phi" in param_dict:
                cos_p = float(param_dict["cos_phi"])
                if 0 < cos_p < 1:
                    tan_p = math.tan(math.acos(cos_p))
                    q_val = float(param_dict["P"]) * tan_p

            calc_res = calculator.calculate_voltage_drop(
                p_kw=float(param_dict["P"]),
                q_kvar=float(q_val),
                r_ohm=float(param_dict["R"]),
                x_ohm=float(param_dict["X"]),
                u_kv=float(u_val)
            )

            if calc_res.get("success"):
                logger.info(f"Deterministic verification passed: {calc_res['calculation_str']}")
                for step in steps:
                    title = step.get("title", "").lower()
                    expl = step.get("explanation", "").lower()
                    formula = step.get("formula_latex", "")

                    if "tổn thất điện áp" in title or "delta u" in title or "delta u" in formula.lower() or "điện áp" in expl:
                        step["formula_latex"] = calc_res["formula_latex"]
                        step["calculated_value"] = f"{calc_res['delta_u_v']} V"
                        step["substituted_values"] = calc_res["calculation_str"]
                        step["verified_by_tool"] = True

                    elif "phần trăm" in title or "delta u%" in title or "%" in step.get("calculated_value", ""):
                        step["calculated_value"] = f"{calc_res['percent_drop']} %"
                        step["substituted_values"] = f"({calc_res['delta_u_v']} / {float(u_val) * 1000.0}) * 100% = {calc_res['percent_drop']}%"
                        step["verified_by_tool"] = True

                ai_result["final_answer"] = (
                    f"Tổn thất điện áp trên đường dây là {calc_res['delta_u_v']} V "
                    f"(tương đương {calc_res['percent_drop']}% điện áp định mức)."
                )
                ai_result["unit"] = "V"
                warnings.append("Đã kiểm chứng và hiệu chỉnh kết quả bằng Python Deterministic Calculator (FR-10, FR-11).")

        # Trường hợp 2: Tính dòng ngắn mạch 3 pha
        elif ("U_mean" in param_dict or "U_tb" in param_dict) and ("Z_total" in param_dict or "Z" in param_dict):
            u_mean = param_dict.get("U_mean") or param_dict.get("U_tb")
            z_tot = param_dict.get("Z_total") or param_dict.get("Z")
            sc_res = calculator.calculate_short_circuit_current(float(u_mean), float(z_tot))
            if sc_res.get("success"):
                for step in steps:
                    if "ngắn mạch" in step.get("title", "").lower():
                        step["formula_latex"] = sc_res["formula_latex"]
                        step["calculated_value"] = f"{sc_res['i_sc_ka']} kA ({sc_res['i_sc_a']} A)"
                        step["substituted_values"] = sc_res["calculation_str"]
                        step["verified_by_tool"] = True
                ai_result["final_answer"] = f"Dòng ngắn mạch 3 pha đối xứng là {sc_res['i_sc_ka']} kA ({sc_res['i_sc_a']} A)."
                warnings.append("Đã kiểm chứng dòng ngắn mạch bằng Python Calculator.")

        # Trường hợp 3: Tính bù công suất phản kháng Q_c
        elif "P" in param_dict and "cos_phi_1" in param_dict and "cos_phi_2" in param_dict:
            comp_res = calculator.calculate_power_factor_compensation(
                float(param_dict["P"]),
                float(param_dict["cos_phi_1"]),
                float(param_dict["cos_phi_2"])
            )
            if comp_res.get("success"):
                for step in steps:
                    if "bù" in step.get("title", "").lower() or "q_c" in step.get("title", "").lower():
                        step["formula_latex"] = comp_res["formula_latex"]
                        step["calculated_value"] = f"{comp_res['q_c_kvar']} kvar"
                        step["substituted_values"] = comp_res["calculation_str"]
                        step["verified_by_tool"] = True
                ai_result["final_answer"] = f"Dung lượng bù công suất phản kháng cần thiết là {comp_res['q_c_kvar']} kvar."
                warnings.append("Đã kiểm chứng dung lượng bù bằng Python Calculator.")

        # 7. Đóng gói phản hồi chuẩn cấu trúc SolutionResponse (hỗ trợ cả extracted_data và direct parameters)
        extracted_data = {
            "problem_type": ai_result.get("problem_type", "calculation"),
            "raw_text_zh": ai_result.get("raw_text_zh", ""),
            "interpreted_text_vi": ai_result.get("interpreted_text_vi", ""),
            "parameters": parameters,
            "unknowns": ai_result.get("unknowns", []),
            "assumptions": ai_result.get("assumptions", []),
            "confidence_score": confidence_score,
            "requires_user_confirmation": requires_user_confirmation
        }

        solution_response = {
            "session_id": session_id,
            "status": status,
            "problem_type": ai_result.get("problem_type", "calculation"),
            "extracted_data": extracted_data,
            "parameters": parameters,
            "unknowns": ai_result.get("unknowns", []),
            "raw_text_zh": ai_result.get("raw_text_zh", ""),
            "interpreted_text_vi": ai_result.get("interpreted_text_vi", ""),
            "steps": steps,
            "final_answer": ai_result.get("final_answer", "Hoàn thành giải toán."),
            "unit": ai_result.get("unit", ""),
            "textbook_reference": textbook_ref,
            "warnings": warnings,
            "language": language
        }

        # 8. Lưu phiên làm việc vào SQLite database (FR-15)
        try:
            title = extracted_data["interpreted_text_vi"][:60] if extracted_data["interpreted_text_vi"] else "Giải bài tập phân phối điện"
            await save_or_update_session(
                session_id=session_id,
                session_type="image_solver",
                title=title,
                data=solution_response
            )
            logger.info(f"Persisted solution session {session_id} into SQLite database.")
        except Exception as e:
            logger.warning(f"Could not persist session to database: {e}")

        return solution_response

    async def answer_chat(
        self,
        question: str,
        session_id: Optional[str] = None,
        language: str = "vi",
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Hỏi đáp chuyên ngành căn cứ vào nguồn PDF giáo trình duy nhất (FR-12, FR-14, FR-23)
        Hỗ trợ ngữ cảnh hội thoại đa lượt (Multi-turn Chat Context - FR-13)
        """
        if not session_id:
            session_id = str(uuid.uuid4())

        # 1. Truy xuất RAG từ PDF giáo trình tiếng Trung duy nhất
        grounded_context, refs = rag_service.get_grounded_context(question)

        # 2. Xây dựng prompt kèm ngữ cảnh hội thoại đa lượt (Multi-turn Context)
        prompt_parts = []
        
        # Nạp lịch sử trao đổi các lượt trước nếu có
        if history and len(history) > 0:
            prompt_parts.append("LỊCH SỬ HỘI THOẠI TRƯỚC ĐÓ:")
            for msg in history[-6:]:
                role = "Sinh viên" if msg.get("role") == "user" else "Trợ lý AI"
                prompt_parts.append(f"{role}: {msg.get('content', '')}")
            prompt_parts.append("\n" + "=" * 40 + "\n")

        prompt_parts.append(f"CÂU HỎI HIỆN TẠI CỦA SINH VIÊN: {question}\n")

        if grounded_context:
            prompt_parts.append(f"CÁC ĐOẠN TRÍCH TỪ PDF GIÁO TRÌNH TIẾNG TRUNG DUY NHẤT:\n{grounded_context}\n")
            prompt_parts.append("YÊU CẦU: Hãy căn cứ CHÍNH XÁC vào các đoạn trích trên để trả lời đầy đủ, chính xác và trích dẫn số trang tương ứng.")
        else:
            prompt_parts.append("LƯU Ý: Không tìm thấy nội dung phù hợp trong PDF giáo trình. Hãy thông báo rõ cho người dùng theo quy tắc FR-14.")

        final_prompt = "\n".join(prompt_parts)

        # 3. Gọi Gemini Chat API có safe JSON parser
        result = gemini_provider.generate_chat(
            prompt=final_prompt,
            system_instruction=CHAT_SYSTEM_PROMPT_VI
        )

        result["session_id"] = session_id
        result["language"] = language

        # Gán trích dẫn tài liệu chuẩn xác
        if refs and ("PDF" not in result.get("textbook_reference", "")):
            result["textbook_reference"] = refs[0]
        elif not result.get("textbook_reference"):
            result["textbook_reference"] = refs[0] if refs else "PDF giáo trình, trang --"

        # 4. Lưu / cập nhật lịch sử phiên hội thoại vào SQLite database (FR-13, FR-15)
        try:
            existing_db = await get_session_by_id(session_id)
            messages = []
            if existing_db and existing_db.data_json:
                try:
                    loaded = json.loads(existing_db.data_json)
                    messages = loaded.get("messages", [])
                except Exception:
                    messages = []

            messages.append({"role": "user", "content": question})
            messages.append({"role": "model", "content": result.get("direct_answer", "") + " " + result.get("explanation", "")})

            session_data = {
                "session_id": session_id,
                "latest_response": result,
                "messages": messages
            }

            title = question[:50] if len(question) <= 50 else question[:47] + "..."
            await save_or_update_session(
                session_id=session_id,
                session_type="chat",
                title=title,
                data=session_data
            )
            logger.info(f"Saved multi-turn chat session {session_id} (turn count: {len(messages)})")
        except Exception as e:
            logger.warning(f"Could not save chat session to database: {e}")

        return result

orchestrator = AgentOrchestrator()
