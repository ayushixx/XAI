import streamlit as st

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
