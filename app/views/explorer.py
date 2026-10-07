import streamlit as st
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
    st.dataframe(df, use_container_width=True)
