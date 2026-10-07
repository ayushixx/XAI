import streamlit as st
import pandas as pd

def render_market(market):
    st.title("Market Intelligence")
    st.markdown("Explore top demanded skills and roles in the analytics job market.")
    
    if not market:
        st.warning("NO VALIDATED EVIDENCE")
        return
        
    df = pd.DataFrame(market).T
    df = df.sort_values(by="sample_size", ascending=True).tail(10) # Top 10 by size
    
    st.markdown("### Top Skills Demanded")
    st.bar_chart(df['sample_size'], horizontal=True) 
    
    st.dataframe(df[['signal', 'evidence_level', 'interpretation']], use_container_width=True)
