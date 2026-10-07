import streamlit as st
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
    st.dataframe(pd.DataFrame(table_data), use_container_width=True)
