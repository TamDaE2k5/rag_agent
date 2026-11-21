import unittest
from backend.app.providers.gemini_provider import safe_json_loads

class TestSafeJSONParser(unittest.TestCase):
    def test_plain_json(self):
        text = '{"name": "test", "value": 123}'
        res = safe_json_loads(text)
        self.assertEqual(res.get("name"), "test")
        self.assertEqual(res.get("value"), 123)

    def test_markdown_code_block(self):
        text = "Here is the response:\n```json\n{\n  \"status\": \"success\",\n  \"code\": 200\n}\n```\nHope that helps!"
        res = safe_json_loads(text)
        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res.get("code"), 200)

    def test_trailing_commas(self):
        text = '{"items": [1, 2, 3,], "key": "val",}'
        res = safe_json_loads(text)
        self.assertEqual(res.get("key"), "val")
        self.assertEqual(res.get("items"), [1, 2, 3])

    def test_unescaped_latex_backslashes(self):
        text = r'{"formula": "\Delta U = \frac{P \cdot R + Q \cdot X}{U_n}", "answer": "\varphi = 0.85"}'
        res = safe_json_loads(text)
        self.assertIn(r"\Delta", res.get("formula", ""))
        self.assertIn(r"\frac", res.get("formula", ""))

    def test_broken_json_fallback(self):
        text = "This is not json at all"
        res = safe_json_loads(text)
        self.assertIn("error", res)
        self.assertFalse(res.get("success", True))

if __name__ == "__main__":
    unittest.main()
