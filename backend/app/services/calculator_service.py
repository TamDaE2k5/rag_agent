import math
from typing import Dict, Any, Optional, Tuple
from backend.app.core.logger import logger

try:
    import sympy as sp
except ImportError:
    sp = None

class ElectricalCalculator:
    """
    Bộ công cụ tính toán an toàn cho kỹ thuật điện phân phối (FR-10, FR-11)
    Đảm bảo tính toán xác định, không phụ thuộc vào việc LLM tự nhẩm số.
    """
    
    @staticmethod
    def calculate_voltage_drop(
        p_kw: float,
        q_kvar: float,
        r_ohm: float,
        x_ohm: float,
        u_kv: float
    ) -> Dict[str, Any]:
        """
        Tính tổn thất điện áp trên đường dây phân phối:
        Delta U = (P*R + Q*X) / U_n  (V hoặc kV)
        """
        try:
            # U ở kV, P ở kW, Q ở kvar -> delta_u = (P*R + Q*X) / (U_kv * 1000) (kV) -> nhân 1000 ra V
            # delta_u_v = (p_kw * r_ohm + q_kvar * x_ohm) / u_kv (V)
            delta_u_v = (p_kw * r_ohm + q_kvar * x_ohm) / u_kv
            delta_u_kv = delta_u_v / 1000.0
            u_norm_v = u_kv * 1000.0
            percent_drop = (delta_u_v / u_norm_v) * 100.0
            
            return {
                "success": True,
                "delta_u_v": round(delta_u_v, 2),
                "delta_u_kv": round(delta_u_kv, 4),
                "percent_drop": round(percent_drop, 2),
                "formula_latex": r"\Delta U = \frac{P \cdot R + Q \cdot X}{U_n}",
                "calculation_str": f"({p_kw} * {r_ohm} + {q_kvar} * {x_ohm}) / {u_kv} = {round(delta_u_v, 2)} V ({round(percent_drop, 2)}%)"
            }
        except Exception as e:
            logger.error(f"Error calculating voltage drop: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_power_loss(
        p_kw: float,
        q_kvar: float,
        r_ohm: float,
        x_ohm: float,
        u_kv: float
    ) -> Dict[str, Any]:
        """
        Tính tổn thất công suất tác dụng và phản kháng:
        Delta P = ((P^2 + Q^2) / U^2) * R
        Delta Q = ((P^2 + Q^2) / U^2) * X
        """
        try:
            s_sq = (p_kw ** 2 + q_kvar ** 2)
            u_sq = (u_kv * 1000.0) ** 2 # V^2
            delta_p_kw = (s_sq * 1000.0 / u_sq) * r_ohm # kW
            delta_q_kvar = (s_sq * 1000.0 / u_sq) * x_ohm # kvar
            
            return {
                "success": True,
                "delta_p_kw": round(delta_p_kw, 3),
                "delta_q_kvar": round(delta_q_kvar, 3),
                "formula_latex": r"\Delta P = \frac{P^2 + Q^2}{U_n^2} \cdot R, \quad \Delta Q = \frac{P^2 + Q^2}{U_n^2} \cdot X",
                "calculation_str": f"Delta P = {round(delta_p_kw, 3)} kW, Delta Q = {round(delta_q_kvar, 3)} kvar"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_short_circuit_current(
        u_mean_kv: float,
        z_total_ohm: float
    ) -> Dict[str, Any]:
        """
        Tính dòng ngắn mạch 3 pha đối xứng:
        I_sc^(3) = U_tb / (sqrt(3) * Z_total)
        """
        try:
            # U_mean ở kV, Z ở Ohm -> I_sc ở kA
            i_sc_ka = u_mean_kv / (math.sqrt(3) * z_total_ohm)
            i_sc_a = i_sc_ka * 1000.0
            return {
                "success": True,
                "i_sc_ka": round(i_sc_ka, 3),
                "i_sc_a": round(i_sc_a, 1),
                "formula_latex": r"I_{nm}^{(3)} = \frac{U_{tb}}{\sqrt{3} \cdot Z_{\Sigma}}",
                "calculation_str": f"{u_mean_kv} / (1.732 * {z_total_ohm}) = {round(i_sc_ka, 3)} kA ({round(i_sc_a, 1)} A)"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_power_factor_compensation(
        p_kw: float,
        cos_phi_1: float,
        cos_phi_2: float
    ) -> Dict[str, Any]:
        """
        Tính dung lượng bù tụ để nâng hệ số công suất:
        Q_c = P * (tan(phi_1) - tan(phi_2))
        """
        try:
            phi_1 = math.acos(cos_phi_1)
            phi_2 = math.acos(cos_phi_2)
            tan_1 = math.tan(phi_1)
            tan_2 = math.tan(phi_2)
            q_c_kvar = p_kw * (tan_1 - tan_2)
            
            return {
                "success": True,
                "q_c_kvar": round(q_c_kvar, 2),
                "formula_latex": r"Q_c = P \cdot (\tan \varphi_1 - \tan \varphi_2)",
                "calculation_str": f"{p_kw} * ({round(tan_1, 3)} - {round(tan_2, 3)}) = {round(q_c_kvar, 2)} kvar"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def safe_evaluate_formula(expression_str: str, variables: Dict[str, float]) -> Optional[float]:
        """Đánh giá an toàn biểu thức toán học thay số bằng Sympy"""
        try:
            expr = sp.sympify(expression_str)
            result = expr.evalf(subs=variables)
            return float(result)
        except Exception as e:
            logger.warning(f"Could not safely evaluate formula '{expression_str}': {e}")
            return None

calculator = ElectricalCalculator()
