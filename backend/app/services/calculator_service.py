import math
from typing import Dict, Any, Optional, Tuple, List
from backend.app.core.logger import logger

try:
    import sympy as sp
except ImportError:
    sp = None

class ElectricalCalculator:
    """
    Bộ công cụ tính toán an toàn cho kỹ thuật điện phân phối (FR-10, FR-11)
    Bao gồm tính toán tổn thất điện áp, ngắn mạch, bù công suất phản kháng,
    và kiểm tra mã truyền thông dữ liệu (Chẵn lẻ ngang dọc, CRC).
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
            u_sq = (u_kv * 1000.0) ** 2
            delta_p_kw = (s_sq * 1000.0 / u_sq) * r_ohm
            delta_q_kvar = (s_sq * 1000.0 / u_sq) * x_ohm
            
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
            if z_total_ohm <= 0:
                return {"success": False, "error": "Z_total phải lớn hơn 0"}
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
    def calculate_horizontal_vertical_parity(
        matrix: List[List[int]],
        parity_type: str = "odd"
    ) -> Dict[str, Any]:
        """
        Tính toán mã kiểm tra chẵn lẻ ngang dọc (Horizontal-Vertical Parity Check)
        căn cứ theo Bảng 3-2 giáo trình trang 45.
        - Kiểm tra ngang (Horizontal): tính bit kiểm tra cho từng hàng.
        - Kiểm tra dọc (Vertical): tính bit kiểm tra cho từng cột.
        - Chuẩn lẻ (odd): tổng số bit 1 (bao gồm cả bit kiểm tra) là số lẻ -> bit = (sum + 1) % 2
        - Chuẩn chẵn (even): tổng số bit 1 (bao gồm cả bit kiểm tra) là số chẵn -> bit = sum % 2
        """
        try:
            rows = len(matrix)
            if rows == 0:
                return {"success": False, "error": "Ma trận trống"}
            cols = len(matrix[0])

            row_sums = [sum(r) for r in matrix]
            col_sums = [sum(matrix[r][c] for r in range(rows)) for c in range(cols)]

            h_odd = [(s + 1) % 2 for s in row_sums]
            v_odd = [(s + 1) % 2 for s in col_sums]

            h_even = [s % 2 for s in row_sums]
            v_even = [s % 2 for s in col_sums]

            h_bits = h_odd if parity_type == "odd" else h_even
            v_bits = v_odd if parity_type == "odd" else v_even

            return {
                "success": True,
                "rows": rows,
                "cols": cols,
                "parity_type": parity_type,
                "horizontal_parity": h_bits,
                "vertical_parity": v_bits,
                "horizontal_str": " ".join(str(b) for b in h_bits),
                "vertical_str": " ".join(str(b) for b in v_bits),
                "odd_parity": {
                    "horizontal": h_odd,
                    "vertical": v_odd,
                    "horizontal_str": " ".join(str(b) for b in h_odd),
                    "vertical_str": " ".join(str(b) for b in v_odd)
                },
                "even_parity": {
                    "horizontal": h_even,
                    "vertical": v_even,
                    "horizontal_str": " ".join(str(b) for b in h_even),
                    "vertical_str": " ".join(str(b) for b in v_even)
                },
                "formula_latex": r"P_h(i) = \left(\sum_{j=1}^{m} d_{i,j} + 1\right) \bmod 2, \quad P_v(j) = \left(\sum_{i=1}^{l} d_{i,j} + 1\right) \bmod 2",
                "calculation_str": f"Ngang (Blank 1): {' '.join(str(b) for b in h_bits)} | Dọc (Blank 2): {' '.join(str(b) for b in v_bits)}"
            }
        except Exception as e:
            logger.error(f"Error calculating horizontal-vertical parity: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_crc(data_bits: str, generator_poly: str) -> Dict[str, Any]:
        """
        Tính toán mã dư thừa vòng CRC (Cyclic Redundancy Check) bằng phép chia đa thức modulo 2 (XOR)
        căn cứ theo Mục 3.2.2 giáo trình trang 46-47: C(x) = M(x)*x^r + R(x).
        """
        try:
            r = len(generator_poly) - 1
            if r <= 0:
                return {"success": False, "error": "Đa thức sinh phải có ít nhất bậc 1"}

            # M(x) * x^r: thêm r bit 0 vào cuối
            appended_data = list(data_bits + "0" * r)
            poly = list(generator_poly)
            k = len(data_bits)

            # Phép chia modulo 2
            quotient = []
            for i in range(k):
                if appended_data[i] == '1':
                    quotient.append('1')
                    for j in range(len(poly)):
                        bit1 = int(appended_data[i + j])
                        bit2 = int(poly[j])
                        appended_data[i + j] = str(bit1 ^ bit2)
                else:
                    quotient.append('0')

            remainder = "".join(appended_data[-r:])
            codeword = data_bits + remainder

            return {
                "success": True,
                "data_bits": data_bits,
                "generator_poly": generator_poly,
                "quotient": "".join(quotient),
                "remainder": remainder,
                "codeword": codeword,
                "crc_bits": remainder,
                "formula_latex": r"C(x) = M(x) \cdot x^r + R(x), \quad R(x) = \text{rem}\left(\frac{M(x) \cdot x^r}{G(x)}\right)",
                "calculation_str": f"Data: {data_bits}, G(x): {generator_poly} -> CRC: {remainder}, Codeword: {codeword}"
            }
        except Exception as e:
            logger.error(f"Error calculating CRC: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def safe_evaluate_formula(expression_str: str, variables: Dict[str, float]) -> Optional[float]:
        """Đánh giá an toàn biểu thức toán học thay số bằng Sympy"""
        try:
            if sp is None:
                return None
            expr = sp.sympify(expression_str)
            result = expr.evalf(subs=variables)
            return float(result)
        except Exception as e:
            logger.warning(f"Could not safely evaluate formula '{expression_str}': {e}")
            return None

calculator = ElectricalCalculator()
