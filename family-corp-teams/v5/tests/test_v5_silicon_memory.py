import unittest
from silicon_memory.v5_silicon_memory import SiliconMemory

class TestSiliconMemory(unittest.TestCase):
    def setUp(self):
        self.memory = SiliconMemory()

    def test_remember_and_recall(self):
        doc_id = self.memory.remember("test document", {"entity": "Test"}, ["v2"])
        self.assertIsNotNone(doc_id)
        results = self.memory.recall("test")
        self.assertIn('episodic', results)
        self.assertIn('semantic', results)
        self.assertIn('procedural', results)

    def test_search(self):
        self.memory.remember("test document 1", {"entity": "Test"}, ["v2"])
        self.memory.remember("test document 2", {"entity": "Test"}, ["v2"])
        results = self.memory.episodic.search("test")
        self.assertGreater(len(results), 0)

    def test_get_document(self):
        doc_id = self.memory.remember("test document", {"entity": "Test"}, ["v2"])
        doc, timestamp = self.memory.episodic.get(doc_id)
        self.assertEqual(doc, "test document")
        self.assertIsInstance(timestamp, int)

    def test_delete_document(self):
        doc_id = self.memory.remember("test document", {"entity": "Test"}, ["v2"])
        self.memory.episodic.remove(doc_id)
        with self.assertRaises(IndexError):
            self.memory.episodic.get(doc_id)

if __name__ == '__main__':
    unittest.main()