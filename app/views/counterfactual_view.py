import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.counterfactual.counterfactual_engine import get_counterfactual_engine
from src.evaluation.skill_roi import get_skill_roi_engine

def render_counterfactual_simulator():
    st.title("Counterfactual Skill Simulator & ROI Leaderboard")
    st.markdown(
        "Simulates what-if scenarios $\\Delta \\text{Score} = f(X') - f(X)$ by dynamically testing the marginal "
        "employability gain of adding candidate skills and ranking them by **Learning ROI**."
    )

    cf_engine = get_counterfactual_engine()
    roi_engine = get_skill_roi_engine()

    available_skills = [
        "Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Docker", "Kubernetes",
        "FastAPI", "TensorFlow", "PyTorch", "MLOps", "Transformers", "RAG Architectures",
        "Snowflake", "Databricks", "Tableau", "Power BI", "Git", "CI/CD", "Prompt Engineering"
    ]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Candidate Configuration")
        candidate_skills = st.multiselect(
            "Current Candidate Skills:",
            options=available_skills,
            default=["Python", "SQL", "Pandas", "Scikit-Learn"]
        )
        target_role = st.selectbox(
            "Target Role:",
            options=[
                "AI Engineer", "MLOps Engineer", "Data Scientist", 
                "Big Data Architect", "Generative AI Architect", "Data Analyst"
            ]
        )
        sim_btn = st.button("Run Counterfactual Optimization", type="primary")

    # Run simulations
    sim_results = cf_engine.simulate_counterfactuals(
        candidate_skills=candidate_skills,
        target_role=target_role
    )
    
    missing_skills = sim_results.get("missing_skills", [])
    roi_results = roi_engine.compute_skill_roi(
        current_skills=candidate_skills,
        target_skills=candidate_skills + missing_skills
    )

    with col2:
        st.subheader("Baseline vs Potential State")
        curr_score = sim_results["current_state"]["job_fit_score"]
        curr_gap = sim_results["current_state"]["skill_gap_percentage"]

        c_col1, c_col2 = st.columns(2)
        c_col1.metric("Current Job Fit Score", f"{curr_score:.1f}%")
        c_col2.metric("Current Skill Gap", f"{curr_gap:.1f}%")

        bundle = sim_results.get("optimal_minimal_bundle", {})
        if bundle:
            st.success(
                f"**Optimal Minimal Bundle**: Acquire `{' + '.join(bundle.get('bundle', []))}` "
                f"to achieve an estimated **{bundle.get('projected_score', 0):.1f}%** fit (+{bundle.get('total_gain', 0):.1f}% gain)."
            )

    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Counterfactual Impact Chart", "Skill ROI Leaderboard"])

    with tab1:
        st.subheader("Marginal Score Gain (Single Skill Interventions)")
        recs = sim_results.get("top_single_skill_recommendations", [])
        if recs:
            df_recs = pd.DataFrame(recs)
            fig = px.bar(
                df_recs,
                x="marginal_gain",
                y="skill",
                orientation="h",
                text="marginal_gain",
                title=f"Marginal Employability Gain (Delta f(X') - f(X)) for {target_role}",
                labels={"marginal_gain": "Score Improvement (%)", "skill": "Intervention Skill"},
                color="marginal_gain",
                color_continuous_scale="Oranges"
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=350)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                df_recs[["skill", "marginal_gain", "counterfactual_score", "why_recommended"]].rename(
                    columns={
                        "skill": "Recommended Skill",
                        "marginal_gain": "Marginal Gain (%)",
                        "counterfactual_score": "Projected Score (%)",
                        "why_recommended": "Rationale"
                    }
                ),
                use_container_width=True
            )
        else:
            st.info("No missing skills identified for counterfactual testing.")

    with tab2:
        st.subheader("Ranked Return on Investment (Gain / Learning Time)")
        roi_recs = roi_results.get("ranked_skill_roi", [])
        if roi_recs:
            df_roi = pd.DataFrame(roi_recs)
            fig_roi = px.bar(
                df_roi,
                x="skill",
                y="roi_index",
                text="roi_index",
                title="Skill ROI Index (Employability Score Gain ÷ Weeks Required)",
                labels={"roi_index": "ROI Index", "skill": "Skill"},
                color="roi_index",
                color_continuous_scale="Viridis"
            )
            fig_roi.update_layout(height=350)
            st.plotly_chart(fig_roi, use_container_width=True)

            st.dataframe(
                df_roi[["skill", "score_gain", "learning_time_weeks", "roi_index", "difficulty"]].rename(
                    columns={
                        "skill": "Skill",
                        "score_gain": "Gain (+%)",
                        "learning_time_weeks": "Duration (Weeks)",
                        "roi_index": "ROI Score",
                        "difficulty": "Complexity Tier"
                    }
                ),
                use_container_width=True
            )
