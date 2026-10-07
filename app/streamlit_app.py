import streamlit as st
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config.settings import BASE_DIR
from app.components.navigation import render_navigation

from app.views.workforce_readiness_view import render_workforce_readiness
from app.views.counterfactual_view import render_counterfactual_simulator
from app.views.career_gps_view import render_career_gps
from app.views.shap_explainability_view import render_shap_explainability
from app.views.digital_twin_view import render_digital_twin
from app.views.future_demand_view import render_future_demand
from app.views.llm_advisor_view import render_llm_advisor

from app.views.overview import render_overview
from app.views.market import render_market
from app.views.capability import render_capability
from app.views.success import render_success
from app.views.signal_map import render_signal_map
from app.views.explorer import render_explorer
from app.views.assistant import render_assistant

st.set_page_config(
    page_title="8BIT Workforce Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    artifacts_dir = BASE_DIR / "artifacts"
    
    def safe_load(filename):
        path = artifacts_dir / filename
        if path.exists():
            with open(path, "r", encoding="utf-8") as file_obj:
                return json.load(file_obj)
        return {}
        
    return (
        safe_load("market_evidence.json"),
        safe_load("jds_evidence.json"),
        safe_load("sds_evidence.json"),
        safe_load("signal_map.json")
    )

market_data, jds_data, sds_data, signal_map_data = load_data()

st.markdown('''
<style>
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #1E1E1E;
    color: #888;
    text-align: center;
    padding: 10px;
    font-size: 0.8rem;
    border-top: 1px solid #333;
    z-index: 1000;
}
.st-emotion-cache-16txtl3 { padding-bottom: 4rem; }
.card-title { color: #D35400; font-weight: bold; }
.caveat-box { border-left: 4px solid #D35400; padding: 10px; background-color: #2C3E50; margin-top: 10px; font-size: 0.9em; }
</style>
<div class="footer">8BIT Workforce Intelligence Platform | Real-Time Decision Support & Machine Learning Analytics</div>
''', unsafe_allow_html=True)

page = render_navigation()

if page == "Workforce Readiness":
    render_workforce_readiness()
elif page == "Counterfactual Simulator":
    render_counterfactual_simulator()
elif page == "Career GPS":
    render_career_gps()
elif page == "SHAP Explainability":
    render_shap_explainability()
elif page == "Personality Digital Twin":
    render_digital_twin()
elif page == "Future Demand Forecast":
    render_future_demand()
elif page == "LLM Career Advisor":
    render_llm_advisor()
elif page == "Overview":
    render_overview(market_data, jds_data, sds_data)
elif page == "Market Intelligence":
    render_market(market_data)
elif page == "Capability Intelligence":
    render_capability(jds_data)
elif page == "Senior Success":
    render_success(sds_data)
elif page == "8BIT Signal Map":
    render_signal_map(signal_map_data)
elif page == "Evidence Explorer":
    render_explorer(signal_map_data)
elif page == "AI Workforce Assistant":
    render_assistant()
