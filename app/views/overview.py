import streamlit as st

def render_overview(market, jds, sds):
    st.markdown("<h1 style='text-align: center; color: #D35400;'>8BIT WORKFORCE INTELLIGENCE</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Evidence-driven workforce and career intelligence</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    cols = st.columns(4)
    cols[0].metric("Market Evidence", len(market))
    cols[1].metric("JDS Evidence", len(jds))
    cols[2].metric("SDS Evidence", len(sds))
    cols[3].metric("Evidence Engine", "VALIDATED")
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>The 8BIT Framework</h2>", unsafe_allow_html=True)
    
    fw_cols = st.columns(4)
    with fw_cols[0]:
        st.info("### MARKET SIGNAL\\n**What industry demands**")
    with fw_cols[1]:
        st.success("### CAPABILITY SIGNAL\\n**What associates with junior outcomes**")
    with fw_cols[2]:
        st.warning("### SUCCESS SIGNAL\\n**Observed senior-success associations**")
    with fw_cols[3]:
        st.error("### EVIDENCE FUSION\\n**Where signals align or diverge**")
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Explore Workforce Signals</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Use the sidebar navigation to explore Market, Capability, and Success intelligence, or ask the AI Assistant.</p>", unsafe_allow_html=True)
