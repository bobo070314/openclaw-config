import unittest
from silicon_memory.v5_silicon_tools import MemConsolidator, TimeSeriesSearch, SkillFusion

class TestMemConsolidator(unittest.TestCase):
    def setUp(self):
        self.consolidator = MemConsolidator()

    def test_add_memory(self):
        self.consolidator.add_memory("test_memory")
        self.assertIn("test_memory", self.consolidator.memory_levels['hot'])

    def test_migrate_memory(self):
        self.consolidator.add_memory("test_memory")
        self.consolidator.migrate_memory()
        self.assertNotIn("test_memory", self.consolidator.memory_levels['hot'])

    def test_calculate_heat(self):
        self.consolidator.add_memory("test_memory")
        heat = self.consolidator.calculate_heat("test_memory")
        self.assertGreater(heat, 0)

class TestTimeSeriesSearch(unittest.TestCase):
    def setUp(self):
        self.search = TimeSeriesSearch([])

    def test_filter_by_time(self):
        self.search.memories = ["memory1", "memory2"]
        filtered = self.search.filter_by_time(100, 200)
        self.assertEqual(filtered, ["memory1", "memory2"])

    def test_detect_hotspots(self):
        self.search.memories = ["memory1", "memory2"]
        hotspots = self.search.detect_hotspots(100)
        self.assertEqual(hotspots, ["memory1", "memory2"])

class TestSkillFusion(unittest.TestCase):
    def setUp(self):
        self.fusion = SkillFusion([])

    def test_merge_skills(self):
        self.fusion.skills = ["skill1", "skill1", "skill2"]
        merged = self.fusion.merge_skills()
        self.assertEqual(len(merged["skill1"]), 2)
        self.assertEqual(len(merged["skill2"]), 1)

    def test_fuse_instructions(self):
        self.fusion.skills = ["skill1", "skill1", "skill2"]
        fused = self.fusion.fuse_instructions("skill1")
        self.assertEqual(fused, "skill1\\nskill1")

if __name__ == '__main__':
    unittest.main()