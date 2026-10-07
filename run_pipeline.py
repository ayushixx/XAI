import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import src.utils.env_setup  # Preload dynamic libraries on macOS
from src.utils.logger import get_logger
from src.audit.data_inventory import discover_and_inventory
from src.cleaning.clean_data_science_jobs import clean_ds_jobs
from src.cleaning.clean_analytics_jobs import clean_analytics_jobs
from src.cleaning.clean_jds import clean_jds
from src.cleaning.clean_sds import clean_sds
from src.eda.generate_charts import run_eda
from src.statistics.statistical_analysis import run_statistics
from src.modeling.jds_modeling import train_jds
from src.modeling.sds_modeling import train_sds
from src.signal_engine.generate_signals import run_signal_engine

# Advanced Enhancements
from src.advanced_modeling.advanced_models import run_advanced_modeling
from src.knowledge_graph.graph_engine import get_knowledge_graph
from src.future_demand.future_demand_engine import get_demand_engine
from src.hwef.hwef_engine import get_hwef_engine
from src.counterfactual.counterfactual_engine import get_counterfactual_engine
from src.career_gps.career_gps_engine import get_career_gps_engine

logger = get_logger(__name__)

def main():
    logger.info('=====================================')
    logger.info('8BIT PIPELINE STARTING')
    logger.info('=====================================')
    
    # 1. Discover and Inventory
    discover_and_inventory()
    
    # 2. Clean Datasets
    clean_ds_jobs()
    clean_analytics_jobs()
    clean_jds()
    clean_sds()
    
    # 3. EDA
    run_eda()
    
    # 4. Statistics
    run_statistics()
    
    # 5. Modeling (Baseline)
    train_jds()
    train_sds()
    
    # 6. Signal Engine
    run_signal_engine()

    # 7. Advanced Modeling (XGBoost, LightGBM, CatBoost & Enhanced Metrics)
    logger.info('Running Phase 7: Advanced Gradient Boosting & Enhanced Metrics')
    run_advanced_modeling()

    # 8. Skill Knowledge Graph Discovery
    logger.info('Running Phase 8: Knowledge Graph Construction & Prerequisite Indexing')
    kg = get_knowledge_graph()
    kg.save_graph()

    # 9. Future Skill Demand Analytics & Forecasting
    logger.info('Running Phase 9: Future Skill Demand & Workforce Velocity Forecasting')
    demand_engine = get_demand_engine()
    demand_engine.generate_workforce_forecast()

    # 10. Hybrid Weighted Evaluation Fusion Initialization
    logger.info('Running Phase 10: HWEF Engine Calibration & Readiness Testing')
    hwef = get_hwef_engine()

    # 11. Counterfactual Skill Recommendation Engine
    logger.info('Running Phase 11: Counterfactual Explainability & What-If Simulation')
    cf_engine = get_counterfactual_engine()
    cf_sample = cf_engine.simulate_counterfactuals(
        candidate_skills=["Python", "SQL"],
        required_skills=["Python", "SQL", "TensorFlow", "Docker", "MLOps"],
        target_role="Senior Machine Learning Engineer"
    )
    logger.info(f"Counterfactual optimal bundle: {cf_sample['optimal_minimal_bundle']['recommended_bundle']} (+{cf_sample['optimal_minimal_bundle']['total_score_boost']}% gain)")

    # 12. Career GPS Shortest Path Navigation
    logger.info('Running Phase 12: Career GPS Graph Optimization (Dijkstra / A*)')
    gps_engine = get_career_gps_engine()
    gps_sample = gps_engine.navigate_career_path(
        current_skills=["Python", "SQL"],
        target_role="AI Engineer",
        algorithm="dijkstra"
    )
    logger.info(f"Career GPS Path: {' -> '.join([step['skill'] for step in gps_sample['gps_trajectory']])} ({gps_sample['estimated_learning_time_months']} months)")
    
    print("\n=======================================================")
    print("8BIT AI WORKFORCE & SKILL GAP SUITE COMPLETE")
    print("=======================================================")
    print("Pipeline executed successfully.")
    print("• Classical & Advanced Models (LR, DT, RF, XGB, LGBM, CatBoost) saved to models/")
    print("• Interactive Knowledge Graph & Prerequisite Trees saved to data/knowledge_graph/")
    print("• 5-Year Future Skill Demand Forecasts saved to reports/future_demand/")
    print("• Counterfactual Optimization & Minimal Skill Bundle Simulator Active")
    print("• Career GPS Shortest Path Navigation (Dijkstra / A*) Active")
    print("• Evaluation & Attribution Reports saved to reports/models/")
    print("• Web UI & REST API ready: launch with 'uvicorn src.api.app:app --reload'")
    print("=======================================================")

if __name__ == '__main__':
    main()

