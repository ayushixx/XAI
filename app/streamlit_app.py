import streamlit as st
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config.settings import BASE_DIR
from app.components.navigation import render_navigation

from app.views.overview import render_overview
from app.views.market import render_market
from app.views.capability import render_capability
from app.views.success import render_success
from app.views.signal_map import render_signal_map
from app.views.explorer import render_explorer
from app.views.assistant import render_assistant

st.set_page_config(page_title="8BIT Workforce Intelligence", layout="wide")

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
<div class="footer">8BIT Evidence Engine | Evidence-backed decision support | No causal claims</div>
''', unsafe_allow_html=True)

page = render_navigation()

if page == "Overview":
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
