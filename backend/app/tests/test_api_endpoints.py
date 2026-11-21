import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.database import init_db
import asyncio

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        asyncio.run(init_db())
        cls.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_history_crud(self):
        # 1. Get history list
        response = self.client.get("/api/v1/history")
        self.assertEqual(response.status_code, 200)
        items = response.json()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

        # 2. Get session detail
        first_id = items[0]["id"]
        detail_res = self.client.get(f"/api/v1/history/{first_id}")
        self.assertEqual(detail_res.status_code, 200)
        detail_data = detail_res.json()
        self.assertEqual(detail_data["session_id"], first_id)

    def test_chat_endpoint(self):
        payload = {
            "question": "Dao cắt tự đóng lại Recloser có công dụng gì?",
            "language": "vi"
        }
        res = self.client.post("/api/v1/chat", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("direct_answer", data)
        self.assertIn("session_id", data)
        self.assertIn("textbook_reference", data)

    def test_confirm_parameters(self):
        payload = {
            "session_id": "test-session-confirm",
            "parameters": [
                {"name": "Điện áp", "symbol": "U_n", "value": 10.0, "unit": "kV", "is_confirmed": True},
                {"name": "Công suất", "symbol": "P", "value": 1000.0, "unit": "kW", "is_confirmed": True},
                {"name": "Điện trở", "symbol": "R", "value": 2.0, "unit": "Ohm", "is_confirmed": True},
                {"name": "Điện kháng", "symbol": "X", "value": 3.0, "unit": "Ohm", "is_confirmed": True}
            ],
            "language": "vi"
        }
        res = self.client.post("/api/v1/solver/confirm-parameters", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")

if __name__ == "__main__":
    unittest.main()
