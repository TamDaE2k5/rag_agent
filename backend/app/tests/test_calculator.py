import unittest
from backend.app.services.calculator_service import calculator

class TestElectricalCalculator(unittest.TestCase):
    def test_voltage_drop(self):
        res = calculator.calculate_voltage_drop(
            p_kw=1200.0,
            q_kvar=744.0,
            r_ohm=2.5,
            x_ohm=3.2,
            u_kv=10.0
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["delta_u_v"], 538.08)
        self.assertEqual(res["percent_drop"], 5.38)

    def test_voltage_drop_zero_voltage(self):
        res = calculator.calculate_voltage_drop(
            p_kw=1200.0,
            q_kvar=744.0,
            r_ohm=2.5,
            x_ohm=3.2,
            u_kv=0.0
        )
        self.assertFalse(res["success"])
        self.assertIn("error", res)

    def test_power_loss(self):
        res = calculator.calculate_power_loss(
            p_kw=1200.0,
            q_kvar=744.0,
            r_ohm=2.5,
            x_ohm=3.2,
            u_kv=10.0
        )
        self.assertTrue(res["success"])
        self.assertGreater(res["delta_p_kw"], 0)
        self.assertGreater(res["delta_q_kvar"], 0)
        self.assertIn("formula_latex", res)

    def test_short_circuit_current(self):
        res = calculator.calculate_short_circuit_current(
            u_mean_kv=10.5,
            z_total_ohm=1.2
        )
        self.assertTrue(res["success"])
        self.assertAlmostEqual(res["i_sc_ka"], 5.052, places=3)
        self.assertAlmostEqual(res["i_sc_a"], 5051.8, places=1)

    def test_short_circuit_zero_impedance(self):
        res = calculator.calculate_short_circuit_current(
            u_mean_kv=10.5,
            z_total_ohm=0.0
        )
        self.assertFalse(res["success"])

    def test_power_factor_compensation(self):
        res = calculator.calculate_power_factor_compensation(
            p_kw=500.0,
            cos_phi_1=0.7,
            cos_phi_2=0.95
        )
        self.assertTrue(res["success"])
        self.assertGreater(res["q_c_kvar"], 0)

    def test_horizontal_vertical_parity(self):
        matrix = [
            [1, 1, 0, 0, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1]
        ]
        res = calculator.calculate_horizontal_vertical_parity(matrix, parity_type="odd")
        self.assertTrue(res["success"])
        self.assertEqual(res["rows"], 5)
        self.assertEqual(res["cols"], 10)
        self.assertEqual(res["odd_parity"]["horizontal"], [0, 0, 0, 1, 1])
        self.assertEqual(res["even_parity"]["horizontal"], [1, 1, 1, 0, 0])
        self.assertEqual(len(res["vertical_parity"]), 10)

    def test_crc_calculation(self):
        # Test CRC with data: 101100010, poly: 10011 (x^4 + x + 1)
        res = calculator.calculate_crc(data_bits="101100010", generator_poly="10011")
        self.assertTrue(res["success"])
        self.assertEqual(len(res["remainder"]), 4)
        self.assertEqual(len(res["codeword"]), 9 + 4)

if __name__ == "__main__":
    unittest.main()
