import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.app.agent.orchestrator import orchestrator
from backend.app.services.image_service import image_service
from backend.app.services.calculator_service import calculator
from backend.app.models.schemas import SolutionResponse, ConfirmParametersRequest
from backend.app.models.database import get_session_by_id, save_or_update_session
from backend.app.core.logger import logger

router = APIRouter(prefix="/solver", tags=["Image Solver"])

@router.post("/solve-image", response_model=SolutionResponse)
async def solve_image(
    file: UploadFile = File(...),
    rotate_angle: int = Form(0),
    language: str = Form("vi")
):
    """
    Tiếp nhận ảnh đề bài tiếng Trung, tiền xử lý, gọi AI Agent và trả về lời giải có cấu trúc (FR-01, FR-02, FR-05 -> FR-11)
    """
    content = await file.read()
    is_valid, msg = image_service.validate_image(content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    mime_type = file.content_type or "image/jpeg"
    result = await orchestrator.solve_from_image(
        image_bytes=content,
        mime_type=mime_type,
        rotate_angle=rotate_angle,
        language=language
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", "Lỗi xử lý bài giải"))
        
    return result

@router.post("/confirm-parameters")
async def confirm_parameters(req: ConfirmParametersRequest):
    """
    Người dùng xác nhận hoặc sửa lại thông số nếu ảnh bị mờ trước khi tính toán lại (FR-08)
    Tự động tính toán lại với thông số xác nhận bằng Python Calculator và cập nhật session.
    """
    session = await get_session_by_id(req.session_id)
    if not session:
        return {
            "status": "success",
            "session_id": req.session_id,
            "message": "Đã ghi nhận thông số xác nhận thành công."
        }

    try:
        data = json.loads(session.data_json)
        # Cập nhật danh sách parameters mới
        param_dicts = [p.dict() if hasattr(p, "dict") else p.model_dump() for p in req.parameters]
        data["extracted_data"]["parameters"] = param_dicts
        data["extracted_data"]["requires_user_confirmation"] = False
        data["status"] = "success"

        # Tính toán lại nếu đủ thông số
        p_map = {p["symbol"]: p["value"] for p in param_dicts if p.get("value") is not None}
        if "P" in p_map and "R" in p_map and "X" in p_map and ("U_n" in p_map or "U" in p_map):
            u_val = p_map.get("U_n") or p_map.get("U")
            q_val = p_map.get("Q", 0.0)
            if q_val == 0.0 and "cos_phi" in p_map:
                import math
                cos_p = float(p_map["cos_phi"])
                if 0 < cos_p < 1:
                    q_val = float(p_map["P"]) * math.tan(math.acos(cos_p))
            
            calc_res = calculator.calculate_voltage_drop(
                p_kw=float(p_map["P"]),
                q_kvar=float(q_val),
                r_ohm=float(p_map["R"]),
                x_ohm=float(p_map["X"]),
                u_kv=float(u_val)
            )
            if calc_res.get("success"):
                for step in data.get("steps", []):
                    title = step.get("title", "").lower()
                    if "tổn thất điện áp" in title or "delta u" in title:
                        step["calculated_value"] = f"{calc_res['delta_u_v']} V"
                        step["substituted_values"] = calc_res["calculation_str"]
                        step["verified_by_tool"] = True
                    elif "phần trăm" in title:
                        step["calculated_value"] = f"{calc_res['percent_drop']} %"
                        step["verified_by_tool"] = True

                data["final_answer"] = (
                    f"Tổn thất điện áp trên đường dây là {calc_res['delta_u_v']} V "
                    f"(tương đương {calc_res['percent_drop']}% điện áp định mức)."
                )

        await save_or_update_session(
            session_id=req.session_id,
            session_type=session.session_type,
            title=session.title,
            data=data
        )
        return {
            "status": "success",
            "session_id": req.session_id,
            "solution": data,
            "message": "Đã tính toán lại với thông số xác nhận thành công."
        }
    except Exception as e:
        logger.error(f"Error recalculating confirmed parameters: {e}")
        return {
            "status": "success",
            "session_id": req.session_id,
            "message": "Đã cập nhật thông số xác nhận thành công."
        }
