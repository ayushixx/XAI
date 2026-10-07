import streamlit as st
from src.ai.assistant import process_query

def render_assistant():
    st.title("AI Workforce Assistant")
    st.markdown("Ask evidence-backed questions about careers, skills, and success in Data Science & Analytics.")
    
    st.warning("⚠️ **DISCLAIMER:** The AI will only answer using validated evidence from the 8BIT Signal Engine. It cannot fabricate statistics, rankings, or causal claims.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Demo-safe suggested questions
    st.markdown("### Demo Questions")
    cols = st.columns(2)
    with cols[0]:
        if st.button("What skills are most demanded?"):
            prompt = "What skills are most demanded?"
        if st.button("Why is Mathematics & Statistics strong?"):
            prompt = "Why is Mathematics & Statistics strong?"
        if st.button("Why is Coding exploratory?"):
            prompt = "Why is Coding exploratory?"
    with cols[1]:
        if st.button("What evidence exists for senior success?"):
            prompt = "What evidence exists for senior success?"
        if st.button("What should I prioritize for a Data Science career?"):
            prompt = "What should I prioritize for a Data Science career?"

    # React to user input or button click
    user_input = st.chat_input("Ask a question (e.g., 'Why is coding only exploratory?'):")
    if user_input:
        prompt = user_input
        
    if 'prompt' in locals() and prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Process via AI Assistant
        response = process_query(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
