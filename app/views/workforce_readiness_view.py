import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.evaluation.workforce_index import get_workforce_index_engine

def render_workforce_readiness():
    st.title("Workforce Readiness Index (WRI)")
    st.markdown(
        "Quantitative psychological and behavioral assessment evaluating workplace readiness based on "
        "the **Big Five (OCEAN)** personality framework."
    )

    wri_engine = get_workforce_index_engine()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Candidate Personality Profile (1 - 10 Scale)")
        c = st.slider("Conscientiousness (Weight: 30%)", 1.0, 10.0, 8.2, 0.1)
        o = st.slider("Openness to Experience (Weight: 25%)", 1.0, 10.0, 7.8, 0.1)
        e = st.slider("Extraversion (Weight: 20%)", 1.0, 10.0, 6.9, 0.1)
        a = st.slider("Agreeableness (Weight: 15%)", 1.0, 10.0, 7.5, 0.1)
        n = st.slider("Neuroticism / Stress Sensitivity (Penalty: -10%)", 1.0, 10.0, 3.2, 0.1)

        compute_btn = st.button("Calculate Workforce Readiness", type="primary")

    res = wri_engine.compute_wri(
        conscientiousness=c,
        openness=o,
        extraversion=e,
        agreeableness=a,
        neuroticism=n
    )

    with col2:
        st.subheader("Readiness Index Score")
        score = res["workforce_readiness_score"]
        tier = res["readiness_tier"]

        st.metric(label="Calculated WRI Score", value=f"{score:.1f} / 100", delta=f"{tier.split('(')[0].strip()}")
        st.info(f"**Classification**: {res['readiness_tier']} (Status: {res['readiness_status']})")

        # Radar Chart
        categories = ['Conscientiousness', 'Openness', 'Extraversion', 'Agreeableness', 'Emotional Stability (10-N)']
        values = [c, o, e, a, max(10.0 - n, 1.0)]
        values += [values[0]] # Close the loop
        categories_closed = categories + [categories[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(211, 84, 0, 0.25)',
            line=dict(color='#D35400', width=2),
            name='Candidate Trait Shape'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=30, b=30),
            height=320
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Mathematical Formulation")
    st.latex(r"WRI_{raw} = 0.30 \cdot C + 0.25 \cdot O + 0.20 \cdot E + 0.15 \cdot A - 0.10 \cdot N")
    st.latex(r"WRI_{normalized} = \frac{WRI_{raw} - WRI_{min}}{WRI_{max} - WRI_{min}} \times 100")
