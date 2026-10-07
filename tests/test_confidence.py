import unittest
from src.signal_engine.confidence import get_confidence

class TestConfidence(unittest.TestCase):
    def test_confidence_logic(self):
        self.assertEqual(get_confidence("STRONG", 0.90, 150), "HIGH")
        self.assertEqual(get_confidence("STRONG", 0.80, 150), "MODERATE")
        self.assertEqual(get_confidence("EXPLORATORY", 0.90, 150), "MODERATE")
        self.assertEqual(get_confidence("WEAK", 0.50, 20), "LOW")
