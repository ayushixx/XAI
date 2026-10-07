import streamlit as st

def render_navigation():
    st.sidebar.title("8BIT Workforce Intelligence")
    st.sidebar.markdown("**Decision Support & Intelligence Platform**")
    
    pages = [
        "Workforce Readiness",
        "Counterfactual Simulator",
        "Career GPS",
        "SHAP Explainability",
        "Personality Digital Twin",
        "Future Demand Forecast",
        "LLM Career Advisor",
        "Overview", 
        "Market Intelligence", 
        "Capability Intelligence", 
        "Senior Success", 
        "8BIT Signal Map", 
        "Evidence Explorer",
        "AI Workforce Assistant"
    ]
    selection = st.sidebar.radio("Navigation", pages)
    return selection
