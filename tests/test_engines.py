import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from src.api.app import app
from src.counterfactual.counterfactual_engine import get_counterfactual_engine
from src.career_gps.career_gps_engine import get_career_gps_engine
from src.hwef.hwef_engine import get_hwef_engine


class TestAnalyticsEngines(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.cf_engine = get_counterfactual_engine()
        cls.gps_engine = get_career_gps_engine()
        cls.hwef_engine = get_hwef_engine()

    def test_hwef_evaluation(self):
        result = self.hwef_engine.evaluate_candidate(
            candidate_skills=["Python", "SQL"],
            required_skills=["Python", "SQL", "Docker", "MLOps"],
            candidate_years_exp=3.0,
            required_years_exp=4.0,
            target_role="MLOps Engineer"
        )
        self.assertIn("job_fit_score", result)
        self.assertIn("skill_gap_percentage", result)
        self.assertGreaterEqual(result["job_fit_score"], 0)
        self.assertLessEqual(result["job_fit_score"], 100)

    def test_counterfactual_simulation(self):
        sim = self.cf_engine.simulate_counterfactuals(
            candidate_skills=["Python", "SQL"],
            required_skills=["Python", "SQL", "Docker", "TensorFlow", "MLOps"],
            target_role="AI Engineer"
        )
        self.assertIn("current_state", sim)
        self.assertIn("top_single_skill_recommendations", sim)
        self.assertIn("optimal_minimal_bundle", sim)
        self.assertIn("top_synergistic_combinations", sim)
        
        # Marginal gain should be non-negative
        for rec in sim["top_single_skill_recommendations"]:
            self.assertGreaterEqual(rec["marginal_gain"], 0)
            self.assertIn("why_recommended", rec)

    def test_career_gps_dijkstra_navigation(self):
        gps = self.gps_engine.navigate_career_path(
            current_skills=["Python", "SQL"],
            target_role="AI Engineer",
            algorithm="dijkstra"
        )
        self.assertEqual(gps["target_role"], "AI Engineer")
        self.assertGreater(gps["path_length"], 0)
        self.assertGreater(gps["estimated_learning_time_weeks"], 0)
        self.assertGreater(len(gps["gps_trajectory"]), 0)
        self.assertIn("expected_salary_growth_pct", gps)

    def test_career_gps_astar_navigation(self):
        gps = self.gps_engine.navigate_career_path(
            current_skills=["Python"],
            target_role="AI Engineer",
            algorithm="astar"
        )
        self.assertGreater(gps["path_length"], 0)
        self.assertGreater(gps["estimated_learning_time_weeks"], 0)

    def test_api_counterfactual_endpoint(self):
        res = self.client.post("/api/v2/counterfactual/simulate", json={
            "candidate_skills": ["Python", "SQL"],
            "required_skills": ["Python", "SQL", "Docker", "TensorFlow"],
            "target_role": "AI Engineer"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("top_single_skill_recommendations", data)
        self.assertIn("optimal_minimal_bundle", data)

    def test_api_career_gps_endpoints(self):
        # Roles endpoint
        r_res = self.client.get("/api/v2/career-gps/roles")
        self.assertEqual(r_res.status_code, 200)
        self.assertIn("roles", r_res.json())

        # Navigate endpoint
        n_res = self.client.post("/api/v2/career-gps/navigate", json={
            "candidate_skills": ["Python", "SQL"],
            "target_role": "AI Engineer",
            "algorithm": "dijkstra"
        })
        self.assertEqual(n_res.status_code, 200)
        self.assertIn("gps_trajectory", n_res.json())


if __name__ == "__main__":
    unittest.main()
