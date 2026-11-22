import unittest
import asyncio
from backend.app.services.calculator_service import calculator
from backend.app.providers.gemini_provider import gemini_provider
from backend.app.agent.orchestrator import orchestrator

class TestParityCheckAndRestAPI(unittest.TestCase):
    """
    Unit & integration tests for:
    1. Horizontal-Vertical Parity Check (Table 3-2, p. 45)
    2. Cyclic Redundancy Check (CRC, p. 46-47)
    3. Direct REST API fallback (Zero Google SDK dependencies)
    4. Real exam exercise verification (anh_bai_tap_mau.jpeg)
    """

    def setUp(self):
        # 5x10 information bit matrix from Table 3-2 in course textbook (p. 45)
        self.table_matrix = [
            [1, 1, 0, 0, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1]
        ]

    def test_horizontal_vertical_parity_calculation(self):
        """Test mathematical parity check with a controlled test matrix"""
        test_matrix = [
            [1, 0, 1],
            [0, 1, 1]
        ]
        # Even parity:
        # row sums = [2, 2] -> even parity bits = [0, 0]
        # col sums = [1, 1, 2] -> even parity bits = [1, 1, 0]
        res_even = calculator.calculate_horizontal_vertical_parity(test_matrix, parity_type="even")
        self.assertTrue(res_even["success"])
        self.assertEqual(res_even["horizontal_parity"], [0, 0])
        self.assertEqual(res_even["vertical_parity"], [1, 1, 0])

        # Odd parity:
        # row sums = [2, 2] -> odd parity bits = [1, 1]
        # col sums = [1, 1, 2] -> odd parity bits = [0, 0, 1]
        res_odd = calculator.calculate_horizontal_vertical_parity(test_matrix, parity_type="odd")
        self.assertTrue(res_odd["success"])
        self.assertEqual(res_odd["horizontal_parity"], [1, 1])
        self.assertEqual(res_odd["vertical_parity"], [0, 0, 1])

    def test_table_3_2_exam_parity(self):
        """Test Table 3-2 matrix calculation corresponding to Blank 1 and Blank 2"""
        res = calculator.calculate_horizontal_vertical_parity(self.table_matrix, parity_type="odd")
        self.assertTrue(res["success"])
        self.assertEqual(res["rows"], 5)
        self.assertEqual(res["cols"], 10)
        self.assertEqual(res["odd_parity"]["horizontal"], [0, 0, 0, 1, 1])
        self.assertEqual(res["even_parity"]["horizontal"], [1, 1, 1, 0, 0])
        self.assertEqual(len(res["vertical_parity"]), 10)

    def test_parity_empty_matrix(self):
        """Test edge case with empty matrix"""
        res = calculator.calculate_horizontal_vertical_parity([])
        self.assertFalse(res["success"])
        self.assertIn("error", res)

    def test_crc_calculation(self):
        """Test Cyclic Redundancy Check modulo-2 polynomial division"""
        data = "11000101"
        poly = "10011"
        res = calculator.calculate_crc(data_bits=data, generator_poly=poly)
        self.assertTrue(res["success"])
        self.assertIn("remainder", res)
        self.assertIn("codeword", res)
        self.assertTrue(res["codeword"].startswith(data))

    def test_crc_invalid_poly(self):
        """Test CRC with invalid degree-0 polynomial"""
        res = calculator.calculate_crc(data_bits="1010", generator_poly="1")
        self.assertFalse(res["success"])

    def test_direct_rest_api_fallback_mode(self):
        """Ensure provider operates in local RAG / fallback mode when key is absent"""
        orig_key = gemini_provider.api_key
        try:
            gemini_provider.api_key = ""
            status = gemini_provider.test_connection()
            self.assertEqual(status["status"], "offline_local_rag")
            self.assertIn("Local RAG", status["message"])

            # Test offline chat at provider level returns use_local_rag flag
            chat_res = gemini_provider.generate_chat("Recloser là gì?")
            self.assertTrue(chat_res.get("use_local_rag"))

            # Test offline chat at orchestrator level completes with dynamic local RAG synthesis
            orch_res = asyncio.run(orchestrator.answer_chat("Recloser là gì?", language="vi"))
            self.assertIn("direct_answer", orch_res)
            self.assertIn("textbook_reference", orch_res)
        finally:
            gemini_provider.api_key = orig_key

    def test_real_exam_image_solve(self):
        """Verify solver accurately solves anh_bai_tap_mau.jpeg with Chapter 3 p. 45 grounding"""
        try:
            with open("sample-data/questions/anh_bai_tap_mau.jpeg", "rb") as f:
                img_bytes = f.read()
        except FileNotFoundError:
            self.skipTest("anh_bai_tap_mau.jpeg not found")

        res = asyncio.run(orchestrator.solve_from_image(
            image_bytes=img_bytes,
            mime_type="image/jpeg",
            language="vi"
        ))
        self.assertEqual(res.get("status"), "success")
        self.assertIn(res.get("problem_type"), ["parity_check", "logic_control"])
        self.assertIn("45", res.get("textbook_reference", ""))

        # Check that Blank 1 and Blank 2 are in the final answer
        final_ans = res.get("final_answer", "")
        self.assertIn("0 0 0 0 1", final_ans)
        self.assertIn("1 0 0 0 1 1 0 1 1 1", final_ans)

        # Ensure verified_by_tool is true
        verified = [s for s in res.get("steps", []) if s.get("verified_by_tool")]
        self.assertGreater(len(verified), 0)

if __name__ == "__main__":
    unittest.main()
