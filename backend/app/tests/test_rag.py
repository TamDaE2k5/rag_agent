import unittest
from backend.app.services.rag_service import rag_service
from backend.app.services.vector_store import vector_store

class TestRAGService(unittest.TestCase):
    def test_vector_store_loaded(self):
        self.assertIsNotNone(vector_store.embeddings)
        self.assertEqual(vector_store.embeddings.shape[0], 233)
        self.assertEqual(vector_store.embeddings.shape[1], 256)
        self.assertEqual(len(vector_store.metadata), 233)

    def test_vectorize_query(self):
        query = "某10kV配电网线路，负荷P = 1200 kW"
        vec = rag_service.vectorize_query(query)
        self.assertEqual(len(vec), 256)
        # Should have non-zero elements
        self.assertGreater(float(vec.sum()), 0.0)

    def test_vector_search(self):
        query = "重合器 分段器 配电自动化"
        results = rag_service.search_vector(query, top_k=3)
        self.assertTrue(len(results) > 0)
        top = results[0]
        self.assertIn("page_number", top)
        self.assertIn("similarity_score", top)
        self.assertIn("reference", top)
        self.assertTrue(top["reference"].startswith("PDF giáo trình, trang"))

    def test_hybrid_search(self):
        query = "电压降 负荷 阻抗"
        results = rag_service.search(query, top_k=3)
        self.assertTrue(len(results) > 0)
        self.assertIn("reference", results[0])

    def test_grounded_context(self):
        query = "Recloser"
        context, refs = rag_service.get_grounded_context(query)
        self.assertIsInstance(context, str)
        self.assertIsInstance(refs, list)

if __name__ == "__main__":
    unittest.main()
