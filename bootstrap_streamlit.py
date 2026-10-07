import os
from pathlib import Path

def create_streamlit_app():
    base_dir = Path("e:/BUILD FOR BHARAT/8BIT_WORKFORCE_SIGNAL_ENGINE")
    app_dir = base_dir / "app"
    components_dir = app_dir / "components"
    views_dir = app_dir / "views"
    streamlit_cfg = base_dir / ".streamlit"
    docs_dir = base_dir / "docs"
    
    for d in [app_dir, components_dir, views_dir, streamlit_cfg, docs_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 1. config.toml
    with open(streamlit_cfg / "config.toml", "w", encoding="utf-8") as f:
        f.write("""[theme]
primaryColor = "#D35400"
backgroundColor = "#1E1E1E"
secondaryBackgroundColor = "#2C3E50"
textColor = "#FFFFFF"
font = "sans serif"
""")

    # 2. components/cards.py
    with open(components_dir / "cards.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st

def evidence_card(title, data):
    st.markdown(f"### {title}")
    
    if data.get("status") == "NO_VALIDATED_EVIDENCE":
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    cols = st.columns(3)
    
    ev_level = data.get('evidence_level', 'UNKNOWN')
    color = "green" if ev_level == "STRONG" else "orange" if ev_level == "EXPLORATORY" else "gray"
    
    cols[0].metric("Evidence Level", ev_level)
    
    pe = data.get('primary_evidence', {})
    if pe.get('odds_ratio') is not None:
        cols[1].metric("Odds Ratio", f"{pe['odds_ratio']:.2f}x")
    if pe.get('p_value') is not None:
        cols[2].metric("Multivariable p-value", f"{pe['p_value']:.4f}")
        
    st.markdown(f"**Interpretation:** {data.get('interpretation', '')}")
    if data.get('caveat'):
        st.markdown(f'<div class="caveat-box"><b>Caveat:</b> {data["caveat"]}</div>', unsafe_allow_html=True)
""")

    # 3. components/navigation.py
    with open(components_dir / "navigation.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st

def render_navigation():
    st.sidebar.title("8BIT Navigation")
    pages = [
        "Overview", 
        "Market Intelligence", 
        "Capability Intelligence", 
        "Senior Success", 
        "8BIT Signal Map", 
        "Evidence Explorer"
    ]
    selection = st.sidebar.radio("Go to", pages)
    return selection
""")

    # 4. views/overview.py
    with open(views_dir / "overview.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st

def render_overview(market, jds, sds):
    st.title("8BIT Workforce Intelligence")
    st.subheader("Evidence-driven career and workforce intelligence for Data Science and Analytics.")
    
    st.markdown("---")
    cols = st.columns(4)
    cols[0].metric("Market Evidence", len(market))
    cols[1].metric("JDS Evidence", len(jds))
    cols[2].metric("SDS Evidence", len(sds))
    cols[3].metric("Evidence Engine", "VALIDATED")
    
    st.markdown("### Model Validation: **COMPLETE**")
    st.markdown("### Causal Claims: **BLOCKED**")
    
    st.markdown("---")
    st.markdown("### The 8BIT Framework")
    st.info("**MARKET SIGNAL:** What employers demand")
    st.info("**CAPABILITY SIGNAL:** What is associated with junior outcomes")
    st.info("**SUCCESS SIGNAL:** What patterns appear in senior outcomes")
    st.info("**EVIDENCE FUSION:** Where signals align or diverge")
    
    st.markdown("---")
    st.markdown("### Explore Career Signals")
    st.markdown("Use the sidebar to navigate through the intelligence layers.")
""")

    # 5. views/market.py
    with open(views_dir / "market.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st
import pandas as pd

def render_market(market):
    st.title("Market Intelligence")
    st.markdown("Explore top demanded skills and roles in the analytics job market.")
    
    if not market:
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    df = pd.DataFrame(market).T
    
    st.markdown("### Top Skills Demanded")
    st.bar_chart(df.head(10)['sample_size']) # Assuming 'sample_size' is the frequency count conceptually
    
    st.dataframe(df[['signal', 'evidence_level', 'interpretation']])
""")

    # 6. views/capability.py
    with open(views_dir / "capability.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st
import pandas as pd
from app.components.cards import evidence_card

def render_capability(jds):
    st.title("Capability Intelligence (JDS)")
    st.markdown("Identify which technical and soft skills independently predict junior outcome success.")
    
    skills = list(jds.keys())
    if not skills:
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    selected_skill = st.selectbox("Select a Skill", skills)
    
    data = jds[selected_skill]
    
    # Explicit check for coding_skills visualization transparency
    if selected_skill == "coding_skills":
        st.warning("Coding Skills demonstrates significant univariate difference but loses independent predictive power in the multivariable model.")
        
    evidence_card(selected_skill.replace("_", " ").title(), data)
    
    st.markdown("---")
    st.markdown("### Evidence Table")
    
    table_data = []
    for k, v in jds.items():
        pe = v.get('primary_evidence', {})
        val = v.get('validation', {})
        table_data.append({
            "Skill": k,
            "Evidence Level": v.get('evidence_level'),
            "OR": pe.get('odds_ratio'),
            "P-value": pe.get('p_value'),
            "CV AUC": val.get('cv_auc')
        })
    st.dataframe(pd.DataFrame(table_data))
""")

    # 7. views/success.py
    with open(views_dir / "success.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st
import pandas as pd
from app.components.cards import evidence_card

def render_success(sds):
    st.title("Senior Success (SDS)")
    st.markdown("Explore personality traits associated with success in senior/customer-facing roles.")
    
    st.warning("⚠️ **DISCLAIMER:** Personality findings are statistical associations in the supplied dataset and are not deterministic career recommendations or psychological diagnoses.")
    
    traits = list(sds.keys())
    if not traits:
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    selected_trait = st.selectbox("Select a Trait", traits)
    
    data = sds[selected_trait]
    evidence_card(selected_trait.replace("_", " ").title(), data)
    
    st.markdown("---")
    st.markdown("### Evidence Table")
    
    table_data = []
    for k, v in sds.items():
        pe = v.get('primary_evidence', {})
        val = v.get('validation', {})
        table_data.append({
            "Trait": k,
            "Evidence Level": v.get('evidence_level'),
            "OR": pe.get('odds_ratio'),
            "P-value": pe.get('p_value'),
            "CV AUC": val.get('cv_auc')
        })
    st.dataframe(pd.DataFrame(table_data))
""")

    # 8. views/signal_map.py
    with open(views_dir / "signal_map.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st

def render_signal_map(signal_map):
    st.title("8BIT Signal Map")
    st.markdown("### Fusion of Market Demand, Junior Capability, and Senior Success")
    st.info("Market demand is not automatically outcome evidence.")
    
    signals = list(signal_map.keys())
    if not signals:
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    selected_signal = st.selectbox("Select a Signal to Fuse", signals)
    
    st.markdown(f"## {selected_signal.replace('_', ' ').title()}")
    
    data = signal_map[selected_signal]
    domain = data.get('domain')
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("### MARKET")
        if domain == "MARKET":
            st.success("High Demand")
            st.write(data.get('interpretation'))
        else:
            st.write("NO VALIDATED EVIDENCE")
            
    with cols[1]:
        st.markdown("### CAPABILITY (JDS)")
        if domain == "JDS":
            ev = data.get('evidence_level')
            if ev == "STRONG": st.success("Strong statistical evidence")
            elif ev == "EXPLORATORY": st.warning("Exploratory evidence")
            else: st.write(ev)
            st.write(data.get('interpretation'))
        else:
            st.write("NO VALIDATED EVIDENCE")
            
    with cols[2]:
        st.markdown("### SUCCESS (SDS)")
        if domain == "SDS":
            ev = data.get('evidence_level')
            if ev == "STRONG": st.success("Validated evidence")
            elif ev == "EXPLORATORY": st.warning("Exploratory evidence")
            else: st.write(ev)
            st.write(data.get('interpretation'))
        else:
            st.write("NO VALIDATED EVIDENCE")
            
    st.markdown("---")
    st.markdown("### OVERALL EVIDENCE STATUS")
    st.markdown(f"**Level:** {data.get('evidence_level')}")
    st.markdown(f"**Interpretation:** {data.get('interpretation')}")
""")

    # 9. views/explorer.py
    with open(views_dir / "explorer.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st
import pandas as pd

def render_explorer(signal_map):
    st.title("Evidence Explorer")
    st.markdown("Technical transparency page for inspecting the raw validated evidence objects.")
    
    if not signal_map:
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    flattened = []
    for k, v in signal_map.items():
        pe = v.get('primary_evidence', {})
        se = v.get('secondary_evidence', {})
        te = v.get('tertiary_evidence', {})
        val = v.get('validation', {})
        
        flattened.append({
            "Signal": k,
            "Domain": v.get('domain'),
            "Evidence Level": v.get('evidence_level'),
            "Model": pe.get('model'),
            "Coef": pe.get('coefficient'),
            "OR": pe.get('odds_ratio'),
            "OR CI Lower": pe.get('ci_lower'),
            "OR CI Upper": pe.get('ci_upper'),
            "Multivariable p": pe.get('p_value'),
            "Univariate p": se.get('p_value'),
            "Tree Importance": te.get('feature_importance'),
            "CV AUC": val.get('cv_auc'),
            "Sample Size": v.get('sample_size'),
            "Caveat": v.get('caveat')
        })
        
    df = pd.DataFrame(flattened)
    st.dataframe(df)
""")

    # 10. streamlit_app.py
    with open(app_dir / "streamlit_app.py", "w", encoding="utf-8") as f:
        f.write("""import streamlit as st
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
""")

    # 11. docs/STREAMLIT_PRODUCT.md
    with open(docs_dir / "STREAMLIT_PRODUCT.md", "w", encoding="utf-8") as f:
        f.write("""# 8BIT Workforce Intelligence Platform

## Architecture
The application is a Streamlit dashboard located in the `app/` directory.
It strictly consumes the `artifacts/` JSON files representing the validated Evidence Store.

## Running the App
```bash
streamlit run app/streamlit_app.py
```

## Pages
1. **Overview**: Landing page showing dataset metrics and the 8BIT framework.
2. **Market Intelligence**: Displays market demand signals.
3. **Capability Intelligence**: Displays validated JDS signals (e.g. Maths-Stats, Coding).
4. **Senior Success**: Displays validated SDS personality signals with strict disclaimers.
5. **8BIT Signal Map**: The fusion page demonstrating the distinction between Market, Capability, and Success.
6. **Evidence Explorer**: Full transparency table of odds ratios, p-values, and CV metrics.

## Design Decisions
- Dark mode enforced via `.streamlit/config.toml`.
- Persistent footer enforcing "No causal claims".
- Caching (`@st.cache_data`) used for JSON loads to ensure performance.
- Direct JSON parsing rather than reinventing the Signal Engine logic, maintaining truth alignment.
""")

    # 12. Create a basic smoke test
    tests_dir = base_dir / "tests"
    with open(tests_dir / "test_ui_smoke.py", "w", encoding="utf-8") as f:
        f.write("""import unittest
from pathlib import Path

class TestUISmoke(unittest.TestCase):
    def test_app_exists(self):
        base = Path("e:/BUILD FOR BHARAT/8BIT_WORKFORCE_SIGNAL_ENGINE")
        self.assertTrue((base / "app/streamlit_app.py").exists())
        self.assertTrue((base / "app/views/capability.py").exists())
        self.assertTrue((base / "app/components/cards.py").exists())
""")

if __name__ == '__main__':
    create_streamlit_app()
