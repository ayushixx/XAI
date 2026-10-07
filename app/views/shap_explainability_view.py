import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.services.shap_service import get_shap_service

def render_shap_explainability():
    st.title("SHAP Machine Learning Explainability")
    st.markdown(
        "Interprets tree-based ensemble predictions (**XGBoost / Random Forest**) using "
        "**Shapley Additive Explanations (SHAP)** from cooperative game theory."
    )

    shap_svc = get_shap_service()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Candidate Capability Inputs (0 - 10 Scale)")
        cand_name = st.text_input("Candidate Name:", value="Alex Chen")
        coding = st.slider("Coding Skills", 0.0, 10.0, 8.5, 0.5)
        aiml = st.slider("AI & Machine Learning Skills", 0.0, 10.0, 9.0, 0.5)
        maths = st.slider("Maths & Statistics Skills", 0.0, 10.0, 8.0, 0.5)
        bigdata = st.slider("Big Data Skills", 0.0, 10.0, 7.0, 0.5)
        dash = st.slider("Dashboard & Storytelling Skills", 0.0, 10.0, 6.5, 0.5)

        explain_btn = st.button("Generate SHAP Attributions", type="primary")

    features = {
        "coding_skills": coding,
        "ai_and_ml_skills": aiml,
        "maths-stats_skills": maths,
        "big_data_skills": bigdata,
        "dashboard_and_storytelling_skills": dash
    }

    explanation = shap_svc.explain_candidate(
        candidate_name=cand_name,
        features=features,
        candidate_skills=["Python", "SQL", "Scikit-Learn"],
        missing_skills=["Docker", "MLOps"]
    )

    with col2:
        st.subheader("Candidate Local Prediction Breakdown")
        base_val = explanation.get("base_value", 0.5)
        pred_val = explanation.get("prediction_value", 0.82)

        p1, p2 = st.columns(2)
        p1.metric("Model Base Value E[f(x)]", f"{base_val:.3f}")
        p2.metric("Candidate Output f(x)", f"{pred_val:.3f}", delta=f"{pred_val - base_val:+.3f}")

        st.info(f"**SHAP Summary Narrative**: {explanation.get('shap_summary', 'Analyzed.')}")

    st.markdown("---")

    tab1, tab2 = st.tabs(["Local Waterfall Attributions", "Global Feature Importance"])

    with tab1:
        st.subheader("Local SHAP Attribution Bar Chart")
        force_data = explanation.get("shap_force_data", {})
        pos_contrib = force_data.get("positive_contributors", [])
        neg_contrib = force_data.get("negative_contributors", [])

        all_contribs = pos_contrib + neg_contrib
        if all_contribs:
            df_contrib = pd.DataFrame(all_contribs)
            
            fig = go.Figure(go.Bar(
                x=df_contrib['shap_value'],
                y=df_contrib['feature'],
                orientation='h',
                marker=dict(
                    color=['#27AE60' if v >= 0 else '#E74C3C' for v in df_contrib['shap_value']]
                ),
                text=[f"{v:+.4f}" for v in df_contrib['shap_value']],
                textposition='auto'
            ))
            fig.update_layout(
                title=f"SHAP Values: How Features Push Prediction from Base E[f(x)]={base_val:.3f} to f(x)={pred_val:.3f}",
                xaxis_title="SHAP Value (Contribution to Probability)",
                yaxis_title="Feature Dimension",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                df_contrib[["feature", "feature_value", "shap_value", "direction"]].rename(
                    columns={
                        "feature": "Capability Feature",
                        "feature_value": "Input Value",
                        "shap_value": "SHAP Impact",
                        "direction": "Impact Direction"
                    }
                ),
                use_container_width=True
            )

    with tab2:
        st.subheader("Global Mean Absolute SHAP Importance")
        global_imp = shap_svc.get_global_feature_importance()
        if global_imp:
            df_glob = pd.DataFrame(global_imp)
            fig_glob = px.bar(
                df_glob,
                x="importance",
                y="feature",
                orientation="h",
                text="importance",
                title="Global Feature Importance (|SHAP| averaged over dataset)",
                labels={"importance": "Mean |SHAP Value|", "feature": "Capability Feature"},
                color="importance",
                color_continuous_scale="Viridis"
            )
            fig_glob.update_layout(yaxis={'categoryorder': 'total ascending'}, height=350)
            st.plotly_chart(fig_glob, use_container_width=True)
