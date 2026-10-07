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

    def test_phase1_skill_embeddings(self):
        from src.semantic_matching.skill_embeddings import get_skill_embedder
        embedder = get_skill_embedder()
        res = embedder.detect_semantic_matches(["ML", "AI"], ["Machine Learning", "Artificial Intelligence", "Docker"])
        self.assertIn("semantic_score", res)
        self.assertGreaterEqual(res["semantic_score"], 50.0)
        self.assertEqual(res["match_count"], 2)

    def test_phase2_skill_graph(self):
        from src.knowledge_graph.skill_graph import get_skill_graph
        kg = get_skill_graph()
        critical = kg.get_critical_skills(top_k=5)
        self.assertEqual(len(critical), 5)
        self.assertIn("composite_centrality", critical[0])
        
        prereqs = kg.get_skill_dependencies("Transformers")
        self.assertIn("PyTorch", prereqs["all_ancestral_prerequisites"])

    def test_phase3_career_gps(self):
        from src.knowledge_graph.career_gps import get_career_gps
        gps = get_career_gps()
        plan = gps.calculate_optimal_learning_path(["Python", "SQL"], "Generative AI Architect")
        self.assertIn("path", plan)
        self.assertIn("estimated_duration", plan)
        self.assertIn("expected_salary_growth", plan)
        self.assertIn("LLMs", plan["path"])

    def test_phase4_counterfactual_delta(self):
        sim = self.cf_engine.simulate_counterfactuals(["Python", "SQL"], ["Python", "SQL", "TensorFlow", "Docker"])
        self.assertIn("top_single_skill_recommendations", sim)
        for rec in sim["top_single_skill_recommendations"]:
            self.assertIn("marginal_gain", rec)
            self.assertIn("counterfactual_score", rec)

    def test_phase5_skill_roi(self):
        from src.evaluation.skill_roi import get_skill_roi_engine
        roi_engine = get_skill_roi_engine()
        res = roi_engine.compute_skill_roi(["Python", "SQL"], ["Python", "SQL", "TensorFlow", "Docker", "MLOps"])
        self.assertIn("ranked_skill_roi", res)
        self.assertGreater(len(res["ranked_skill_roi"]), 0)
        top_roi = res["ranked_skill_roi"][0]
        self.assertIn("roi_index", top_roi)
        self.assertIn("learning_time_weeks", top_roi)
        self.assertGreaterEqual(top_roi["roi_index"], 0)

    def test_phase6_shap_service(self):
        from src.services.shap_service import get_shap_service
        shap_svc = get_shap_service()
        global_imp = shap_svc.get_global_feature_importance()
        self.assertGreater(len(global_imp), 0)
        exp = shap_svc.explain_candidate(
            "Alex Chen",
            {"coding_skills": 8.5, "ai_and_ml_skills": 9.0, "maths-stats_skills": 8.0, "big_data_skills": 7.0, "dashboard_and_storytelling_skills": 6.5},
            candidate_skills=["Python", "SQL"],
            missing_skills=["Docker"]
        )
        self.assertIn("shap_summary", exp)
        self.assertIn("shap_force_data", exp)
        self.assertIn("positive_contributors", exp["shap_force_data"])

    def test_phase7_personality_autoencoder(self):
        from src.modeling.personality_autoencoder import get_personality_autoencoder
        ae = get_personality_autoencoder()
        res = ae.encode_personality(
            "test_user",
            {"Neuroticism": 4.0, "Extraversion": 7.0, "Openness": 8.0, "Agreeableness": 7.5, "Conscientiousness": 8.5}
        )
        self.assertIn("personality_embedding", res)
        self.assertIn("latent_personality_vector", res)
        self.assertEqual(len(res["latent_personality_vector"]), 3)
        self.assertIn("reconstructed_traits", res)

    def test_phase8_workforce_index(self):
        from src.evaluation.workforce_index import get_workforce_index_engine
        wri_eng = get_workforce_index_engine()
        res = wri_eng.compute_wri(conscientiousness=8.0, openness=7.5, extraversion=7.0, agreeableness=7.5, neuroticism=3.5)
        self.assertIn("workforce_readiness_score", res)
        self.assertGreaterEqual(res["workforce_readiness_score"], 0.0)
        self.assertLessEqual(res["workforce_readiness_score"], 100.0)
        self.assertIn("readiness_tier", res)

    def test_phase9_digital_twin(self):
        from src.evaluation.digital_twin import get_digital_twin_engine
        twin_eng = get_digital_twin_engine()
        res = twin_eng.simulate_digital_twin(
            "Alex Chen",
            {"Conscientiousness": 70.0, "Openness": 75.0, "Extraversion": 65.0, "Agreeableness": 70.0, "Neuroticism": 45.0},
            delta_conscientiousness=5.0,
            delta_neuroticism=-5.0
        )
        self.assertIn("current_state", res)
        self.assertIn("future_state", res)
        self.assertIn("improvement", res)
        self.assertGreater(res["future_state"]["future_score"], res["current_state"]["current_score"])
        self.assertIn("success_probability_gain", res["improvement"])

    def test_phase10_trend_forecasting(self):
        from src.future_demand.trend_forecasting import get_demand_forecaster
        engine = get_demand_forecaster()
        forecast = engine.forecast_future_demand()
        self.assertIn("top_emerging_skills", forecast)
        self.assertIn("top_declining_skills", forecast)
        self.assertIn("all_skill_forecasts", forecast)
        self.assertIn("model_comparison", forecast)
        self.assertGreater(len(forecast["top_emerging_skills"]), 0)
        self.assertIn("XGBoost", forecast["model_comparison"])
        self.assertIn("LightGBM", forecast["model_comparison"])

    def test_phase11_llm_advisor(self):
        from src.services.llm_advisor import get_llm_advisor
        advisor = get_llm_advisor()
        advice = advisor.generate_career_intelligence(
            candidate_profile={"name": "Alex Chen", "target_role": "AI Engineer", "baseline_score": 82.0},
            counterfactual_results={"top_single_skill_recommendations": [{"skill": "Docker", "marginal_gain": 9.5}]},
            career_gps_path={"gps_trajectory": [{"step": 1, "skill": "Docker"}]},
            wri={"workforce_readiness_score": 84.5, "readiness_tier": "Tier 1: High Readiness"},
            shap_explanation={"shap_summary": "Top positive factor: Coding"}
        )
        self.assertIn("career_advice", advice)
        self.assertIn("learning_roadmap", advice)
        self.assertIn("interview_preparation", advice)
        self.assertIn("salary_insights", advice)
        self.assertIn("career_risks", advice)

    def test_phase12_rag_service(self):
        from src.services.rag_service import get_rag_service
        rag_svc = get_rag_service()
        ans = rag_svc.answer_query("What skills will be important in 2028?")
        self.assertIn("query", ans)
        self.assertIn("synthesized_answer", ans)
        self.assertIn("retrieved_evidence", ans)
        self.assertIn("knowledge_sources_consulted", ans)
        self.assertGreater(len(ans["knowledge_sources_consulted"]), 0)


if __name__ == "__main__":
    unittest.main()


