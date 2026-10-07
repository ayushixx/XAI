import unittest
from src.ai.assistant import process_query

class TestAIAssistant(unittest.TestCase):
    def test_coding_exploratory_test_case(self):
        # The assistant MUST correctly answer: "Is coding a strong predictor?"
        response = process_query("Is coding a strong predictor?")
        
        # Verify format and specific wording restrictions
        self.assertIn("### Answer", response)
        self.assertIn("EXPLORATORY", response)
        self.assertNotIn("STRONG statistical evidence", response.replace("STRONG", ""))
        self.assertIn("multivariable significance is not established", response.lower())
        
    def test_mathematics_strong_test_case(self):
        # "Why is Mathematics & Statistics a strong capability signal?"
        response = process_query("Why is Mathematics & Statistics a strong capability signal?")
        self.assertIn("STRONG", response)
        self.assertIn("Odds Ratio:", response)
        self.assertIn("6.17", response) # Value check to ensure it retrieves actuals
        
    def test_no_evidence_behavior(self):
        response = process_query("Does knowing React help?")
        self.assertEqual(response, "I do not have validated evidence for that in the supplied datasets.")
        
    def test_causality_guardrail(self):
        response = process_query("Does conscientiousness cause success?")
        self.assertNotIn("cause", response.lower().replace("because", ""))
        self.assertIn("associated with", response)

if __name__ == '__main__':
    unittest.main()
