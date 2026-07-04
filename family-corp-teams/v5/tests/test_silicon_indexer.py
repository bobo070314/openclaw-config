import unittest
from silicon_memory.v5_silicon_indexer import InvertedIndex, TfidfScorer, EntityExtractor, ConflictDetector

class TestInvertedIndex(unittest.TestCase):
    def setUp(self):
        self.index = InvertedIndex()

    def test_add_and_get(self):
        self.index.add("test", 1, 2)
        self.assertEqual(self.index.get("test"), [(1, 2)])

    def test_update(self):
        self.index.add("test", 1, 2)
        self.index.update("test", 1, 3)
        self.assertEqual(self.index.get("test"), [(1, 3)])

    def test_compress(self):
        self.index.add("test", 1, 2)
        self.index.compress()
        self.assertEqual(self.index.get("test"), [(1, 2)])

class TestTfidfScorer(unittest.TestCase):
    def setUp(self):
        self.index = InvertedIndex()
        self.scorer = TfidfScorer(self.index)

    def test_compute(self):
        self.index.add("test", 1, 2)
        self.index.add("test", 2, 1)
        scores = self.scorer.compute(["test"], "test document")
        self.assertTrue("test" in scores)

class TestEntityExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = EntityExtractor()

    def test_extract(self):
        text = "This is a test with CamelCase and_underline, and (parentheses)"
        entities = self.extractor.extract(text)
        self.assertIn("CamelCase", entities)
        self.assertIn("undereline", entities)
        self.assertIn("parentheses", entities)

class TestConflictDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ConflictDetector()

    def test_edit_distance(self):
        self.assertEqual(self.detector.edit_distance("abc", "abc"), 0)
        self.assertEqual(self.detector.edit_distance("abc", "abd"), 1)
        self.assertEqual(self.detector.edit_distance("abc", "abx"), 2)

    def test_content_similarity(self):
        self.assertAlmostEqual(self.detector.content_similarity("abc", "abc"), 1.0)
        self.assertAlmostEqual(self.detector.content_similarity("abc", "abd"), 0.6666666666666666)

if __name__ == '__main__':
    unittest.main()