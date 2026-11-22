import unittest
import io
import os
from PIL import Image
from backend.app.agent.orchestrator import orchestrator
from backend.app.models.database import init_db, get_session_by_id

class TestAgentOrchestrator(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await init_db()
        # Tạo ảnh JPEG 50x50 hợp lệ bằng Pillow
        img = Image.new("RGB", (50, 50), color="white")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        self.sample_jpeg_bytes = buf.getvalue()

    async def test_solve_from_image_mock(self):
        res = await orchestrator.solve_from_image(
            image_bytes=self.sample_jpeg_bytes,
            mime_type="image/jpeg",
            language="vi"
        )
        self.assertIn("session_id", res)
        self.assertIn("extracted_data", res)
        self.assertIn("parameters", res)
        self.assertIn("steps", res)
        self.assertIn("final_answer", res)
        self.assertIn("textbook_reference", res)

        steps = res["steps"]
        verified_steps = [s for s in steps if s.get("verified_by_tool")]
        self.assertTrue(len(verified_steps) > 0)

        # Check SQLite persistence
        db_session = await get_session_by_id(res["session_id"])
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.session_type, "image_solver")

    async def test_solve_real_exam_image(self):
        img_path = "sample-data/questions/anh_bai_tap_mau.jpeg"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                real_img_bytes = f.read()

            res = await orchestrator.solve_from_image(
                image_bytes=real_img_bytes,
                mime_type="image/jpeg",
                language="vi"
            )
            self.assertEqual(res.get("status"), "success")
            self.assertIn("0 0 0 0 1", res.get("final_answer"))
            self.assertIn("1 0 0 0 1 1 0 1 1 1", res.get("final_answer"))
            self.assertEqual(res.get("textbook_reference"), "PDF giáo trình, trang 45")
            self.assertEqual(res.get("problem_type"), "logic_control")

    async def test_multi_turn_chat(self):
        session_id = "test-chat-session-1"
        res1 = await orchestrator.answer_chat(
            question="Recloser là gì trong lưới điện phân phối?",
            session_id=session_id,
            language="vi"
        )
        self.assertEqual(res1["session_id"], session_id)
        self.assertIn("direct_answer", res1)
        self.assertIn("textbook_reference", res1)

        # Multi-turn second question
        history = [
            {"role": "user", "content": "Recloser là gì trong lưới điện phân phối?"},
            {"role": "model", "content": res1["direct_answer"]}
        ]
        res2 = await orchestrator.answer_chat(
            question="Nó phối hợp với thiết bị nào để tự động cô lập sự cố?",
            session_id=session_id,
            language="vi",
            history=history
        )
        self.assertEqual(res2["session_id"], session_id)

        # Verify saved in SQLite with messages
        db_session = await get_session_by_id(session_id)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.session_type, "chat")

if __name__ == "__main__":
    unittest.main()
