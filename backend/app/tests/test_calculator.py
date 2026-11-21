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

    def test_short_circuit_current(self):
        res = calculator.calculate_short_circuit_current(
            u_mean_kv=10.5,
            z_total_ohm=1.2
        )
        self.assertTrue(res["success"])
        self.assertGreater(res["i_sc_ka"], 0)
        self.assertGreater(res["i_sc_a"], 0)

    def test_power_factor_compensation(self):
        res = calculator.calculate_power_factor_compensation(
            p_kw=500.0,
            cos_phi_1=0.7,
            cos_phi_2=0.95
        )
        self.assertTrue(res["success"])
        self.assertGreater(res["q_c_kvar"], 0)

if __name__ == "__main__":
    unittest.main()
