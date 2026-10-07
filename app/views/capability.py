import streamlit as st
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
    st.dataframe(pd.DataFrame(table_data), use_container_width=True)
