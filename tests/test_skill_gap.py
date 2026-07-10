import unittest

from src.models.skill_gap import SkillGapAnalyzer


class SkillGapAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analyzer = SkillGapAnalyzer()

    def test_normalize_skill_filters_generic_terms(self):
        self.assertIsNone(self.analyzer._normalize_skill("management"))
        self.assertIsNone(self.analyzer._normalize_skill("time"))
        self.assertEqual(self.analyzer._normalize_skill("machine learning"), "machine learning")
        self.assertEqual(self.analyzer._normalize_skill("python"), "python")

    def test_get_required_skills_returns_role_specific_terms(self):
        skills = self.analyzer.get_required_skills("senior data scientist machine learning")
        self.assertTrue(skills)
        self.assertFalse(any(skill in {"management", "analytics", "analysis", "time"} for skill in skills))
        self.assertTrue(any("machine" in skill or "python" in skill or "learning" in skill for skill in skills))


if __name__ == "__main__":
    unittest.main()
