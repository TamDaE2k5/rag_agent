import unittest
import io
import asyncio
from unittest.mock import patch
from PIL import Image
from backend.app.agent.orchestrator import orchestrator
from backend.app.providers.gemini_provider import gemini_provider

class TestAgentOrchestrator(unittest.TestCase):
    """
    Offline unit & integration tests for AI Agent Orchestrator.
    Guarantees no live Gemini API quota is consumed by mocking or using fallback responses.
    """

    def setUp(self):
        # Create a valid JPEG image in-memory using PIL
        img = Image.new("RGB", (50, 50), color="white")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        self.sample_jpeg_bytes = buf.getvalue()

    def test_solve_from_image_offline_fallback(self):
        """Test solve_from_image workflow when Gemini API is offline (demo/mock mode)"""
        with patch.object(gemini_provider, "_client", None):
            res = asyncio.run(orchestrator.solve_from_image(
                image_bytes=self.sample_jpeg_bytes,
                mime_type="image/jpeg",
                rotate_angle=0,
                language="vi"
            ))
            self.assertEqual(res.get("status"), "success")
            self.assertEqual(res.get("language"), "vi")
            self.assertIn("session_id", res)
            self.assertIn("extracted_data", res)
            self.assertIn("steps", res)
            self.assertIn("final_answer", res)
            self.assertIn("textbook_reference", res)
            self.assertTrue(res["textbook_reference"].startswith("PDF giáo trình, trang"))

    def test_solve_from_image_error_handling(self):
        """Test graceful handling when LLM returns an error"""
        with patch.object(gemini_provider, "generate_with_image", return_value={"error": "API Quota Exceeded", "success": False}):
            res = asyncio.run(orchestrator.solve_from_image(
                image_bytes=self.sample_jpeg_bytes,
                mime_type="image/jpeg",
                language="vi"
            ))
            self.assertEqual(res.get("status"), "error")
            self.assertIn("API Quota Exceeded", res.get("message"))

    def test_answer_chat_offline_fallback(self):
        """Test answer_chat RAG grounding and response structure"""
        with patch.object(gemini_provider, "_client", None):
            res = asyncio.run(orchestrator.answer_chat(
                question="Nguyên lý hoạt động của Recloser trong lưới điện phân phối là gì?",
                session_id="test-session-123",
                language="vi"
            ))
            self.assertEqual(res.get("session_id"), "test-session-123")
            self.assertEqual(res.get("language"), "vi")
            self.assertIn("direct_answer", res)
            self.assertIn("explanation", res)
            self.assertIn("textbook_reference", res)
            self.assertTrue(res["textbook_reference"].startswith("PDF giáo trình, trang"))

    def test_mock_solution_consistency(self):
        """Verify the mock solution schema matches expected frontend contract"""
        mock_data = gemini_provider._generate_mock_solution()
        self.assertIn("problem_type", mock_data)
        self.assertIn("parameters", mock_data)
        self.assertIn("steps", mock_data)
        self.assertIn("final_answer", mock_data)
        for p in mock_data["parameters"]:
            self.assertIn("name", p)
            self.assertIn("symbol", p)
            self.assertIn("value", p)
            self.assertIn("unit", p)
        for s in mock_data["steps"]:
            self.assertIn("step_number", s)
            self.assertIn("title", s)
            self.assertIn("formula_latex", s)
            self.assertIn("calculated_value", s)

if __name__ == "__main__":
    unittest.main()
