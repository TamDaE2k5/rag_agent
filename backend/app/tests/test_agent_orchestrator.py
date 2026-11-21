import unittest
import asyncio
import io
from PIL import Image
from backend.app.agent.orchestrator import orchestrator
from backend.app.models.database import init_db, get_session_by_id

class TestAgentOrchestrator(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await init_db()

    async def test_solve_from_image_mock(self):
        # Tạo valid PNG bytes
        buf = io.BytesIO()
        img = Image.new("RGB", (20, 20), color="white")
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        res = await orchestrator.solve_from_image(
            image_bytes=png_bytes,
            mime_type="image/png",
            language="vi"
        )
        self.assertIn("session_id", res)
        self.assertIn("extracted_data", res)
        self.assertIn("steps", res)
        self.assertIn("final_answer", res)
        self.assertIn("textbook_reference", res)

        # Check deterministic verification (537.98 V or 538.08 V depending on rounding of tan_phi)
        self.assertTrue("537.98" in res["final_answer"] or "538.08" in res["final_answer"] or "538" in res["final_answer"])
        steps = res["steps"]
        verified_steps = [s for s in steps if s.get("verified_by_tool")]
        self.assertTrue(len(verified_steps) > 0)

        # Check SQLite persistence
        db_session = await get_session_by_id(res["session_id"])
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.session_type, "image_solver")

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
