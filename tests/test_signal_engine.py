import unittest
from src.signal_engine.evidence import get_signal

class TestSignalEngine(unittest.TestCase):
    def test_coding_skills_exploratory(self):
        sig = get_signal("coding_skills")
        self.assertEqual(sig["evidence_level"], "EXPLORATORY")
        self.assertAlmostEqual(sig["primary_evidence"]["odds_ratio"], 1.8385, places=4)
        self.assertAlmostEqual(sig["primary_evidence"]["p_value"], 0.0763, places=4)
        
        ci_lower = sig["primary_evidence"]["ci_lower"]
        ci_upper = sig["primary_evidence"]["ci_upper"]
        self.assertTrue(ci_lower <= 1.0 <= ci_upper, "OR CI must include 1.0 since p >= 0.05")
        
    def test_maths_stats(self):
        sig = get_signal("maths-stats_skills")
        self.assertEqual(sig["primary_evidence"]["model"], "Logistic Regression")
        self.assertEqual(sig["evidence_level"], "STRONG")
        
    def test_causal_is_false(self):
        sig = get_signal("coding_skills")
        self.assertFalse(sig["causal"])
        
    def test_missing_evidence(self):
        sig = get_signal("nonexistent_skill")
        self.assertEqual(sig["status"], "NO_VALIDATED_EVIDENCE")
