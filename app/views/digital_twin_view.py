import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.evaluation.digital_twin import get_digital_twin_engine
from src.modeling.personality_autoencoder import get_personality_autoencoder

def render_digital_twin():
    st.title("Personality Digital Twin & Deep Learning Autoencoder")
    st.markdown(
        "Simulates counterfactual psychological growth and encodes high-dimensional traits into a "
        "compact latent vector space $z \\in \\mathbb{R}^3$ via a **5 $\\to$ 16 $\\to$ 8 $\\to$ 3 Deep Autoencoder**."
    )

    twin_engine = get_digital_twin_engine()
    autoencoder = get_personality_autoencoder()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Baseline Personality Traits (0 - 100 Scale)")
        c = st.slider("Conscientiousness", 0.0, 100.0, 72.0, 1.0)
        o = st.slider("Openness", 0.0, 100.0, 78.0, 1.0)
        e = st.slider("Extraversion", 0.0, 100.0, 65.0, 1.0)
        a = st.slider("Agreeableness", 0.0, 100.0, 70.0, 1.0)
        n = st.slider("Neuroticism", 0.0, 100.0, 48.0, 1.0)

        st.subheader("Digital Twin Simulation Adjustments")
        delta_c = st.slider("Δ Conscientiousness (Target Coaching)", -20.0, 20.0, 8.0, 1.0)
        delta_n = st.slider("Δ Neuroticism (Stress Resilience)", -20.0, 20.0, -8.0, 1.0)

        sim_btn = st.button("Simulate Digital Twin State", type="primary")

    current_traits = {
        "Conscientiousness": c,
        "Openness": o,
        "Extraversion": e,
        "Agreeableness": a,
        "Neuroticism": n
    }

    sim_res = twin_engine.simulate_digital_twin(
        candidate_name="Candidate",
        current_traits=current_traits,
        delta_conscientiousness=delta_c,
        delta_neuroticism=delta_n
    )

    encoded_curr = autoencoder.encode_personality("current_candidate", current_traits)

    with col2:
        st.subheader("Simulation Results")
        curr_score = sim_res["current_state"]["current_score"]
        future_score = sim_res["future_state"]["future_score"]
        gain = sim_res["improvement"]["score_gain"]
        prob_gain = sim_res["improvement"]["success_probability_gain"]

        r1, r2 = st.columns(2)
        r1.metric("Current State Score", f"{curr_score:.1f}")
        r2.metric("Simulated Future State", f"{future_score:.1f}", delta=f"{gain:+.1f}")

        st.success(f"**Projected Career Success Probability Increase**: **{prob_gain}**")

        # Comparative Radar Chart
        categories = ['Conscientiousness', 'Openness', 'Extraversion', 'Agreeableness', 'Emotional Stability']
        curr_vals = [c, o, e, a, max(100.0 - n, 0.0)]
        future_vals = [
            sim_res["future_state"]["simulated_traits"]["Conscientiousness"],
            sim_res["future_state"]["simulated_traits"]["Openness"],
            sim_res["future_state"]["simulated_traits"]["Extraversion"],
            sim_res["future_state"]["simulated_traits"]["Agreeableness"],
            max(100.0 - sim_res["future_state"]["simulated_traits"]["Neuroticism"], 0.0)
        ]
        curr_vals += [curr_vals[0]]
        future_vals += [future_vals[0]]
        categories_closed = categories + [categories[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=curr_vals,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(41, 128, 185, 0.2)',
            line=dict(color='#2980B9', width=2),
            name='Current State'
        ))
        fig.add_trace(go.Scatterpolar(
            r=future_vals,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(39, 174, 96, 0.25)',
            line=dict(color='#27AE60', width=2, dash='dash'),
            name='Future Digital Twin'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            legend=dict(orientation="h", y=-0.1),
            margin=dict(l=40, r=40, t=30, b=30),
            height=340
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Deep Learning Latent Personality Vector Space $z \\in \\mathbb{R}^3$")
    z = encoded_curr.get("latent_personality_vector", [0, 0, 0])
    
    col_z1, col_z2, col_z3 = st.columns(3)
    col_z1.metric("Latent Dimension $z_1$", f"{z[0]:.4f}")
    col_z2.metric("Latent Dimension $z_2$", f"{z[1]:.4f}")
    col_z3.metric("Latent Dimension $z_3$", f"{z[2]:.4f}")

    st.caption("Deep Autoencoder Architecture: Input (5) ➔ Linear (16) ➔ Linear (8) ➔ Bottleneck Latent (3) ➔ Decoder (5)")
