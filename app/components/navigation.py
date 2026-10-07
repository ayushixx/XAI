import streamlit as st

def render_navigation():
    st.sidebar.title("8BIT Navigation")
    pages = [
        "Overview", 
        "Market Intelligence", 
        "Capability Intelligence", 
        "Senior Success", 
        "8BIT Signal Map", 
        "Evidence Explorer",
        "AI Workforce Assistant"
    ]
    selection = st.sidebar.radio("Go to", pages)
    return selection
