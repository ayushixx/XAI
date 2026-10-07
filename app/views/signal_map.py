import streamlit as st

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
