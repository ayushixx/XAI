import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.future_demand.trend_forecasting import get_demand_forecaster

def render_future_demand():
    st.title("Future Skill Demand Forecasting")
    st.markdown(
        "Machine Learning time-series regression and market trend forecasting using **XGBoost** and "
        "**LightGBM** to predict emerging vs. declining skill demand through 2029."
    )

    forecaster = get_demand_forecaster()
    results = forecaster.forecast_future_demand()

    # Model Benchmark Summary
    st.subheader("Model Benchmark: XGBoost vs LightGBM")
    comparison = results.get("model_comparison", {})
    if comparison:
        df_comp = pd.DataFrame(comparison).T.reset_index().rename(columns={"index": "Model Architecture"})
        
        m_cols = st.columns(len(comparison))
        for i, (name, metrics) in enumerate(comparison.items()):
            with m_cols[i]:
                st.metric(
                    label=f"{name} (Rank #{metrics.get('Rank', i+1)})",
                    value=f"R² = {metrics.get('R2_Score', 0):.3f}",
                    delta=f"MAE: {metrics.get('MAE', 0):,.0f}"
                )

        st.dataframe(df_comp, use_container_width=True)

    st.markdown("---")

    # Top Emerging vs Declining
    col_em, col_dec = st.columns(2)

    with col_em:
        st.subheader("Top Emerging Hyper-Growth Skills")
        emerging = results.get("top_emerging_skills", [])
        if emerging:
            df_em = pd.DataFrame(emerging)
            fig_em = px.bar(
                df_em,
                x="growth_cagr_pct",
                y="skill",
                orientation="h",
                text="growth_cagr_pct",
                title="Top Emerging Skills by CAGR Growth (%)",
                labels={"growth_cagr_pct": "Annual Growth Rate (CAGR %)", "skill": "Skill"},
                color="growth_cagr_pct",
                color_continuous_scale="Greens"
            )
            fig_em.update_layout(yaxis={'categoryorder': 'total ascending'}, height=320)
            st.plotly_chart(fig_em, use_container_width=True)

    with col_dec:
        st.subheader("Top Declining & Legacy Skills")
        declining = results.get("top_declining_skills", [])
        if declining:
            df_dec = pd.DataFrame(declining)
            fig_dec = px.bar(
                df_dec,
                x="growth_cagr_pct",
                y="skill",
                orientation="h",
                text="growth_cagr_pct",
                title="Top Declining Skills by CAGR (%)",
                labels={"growth_cagr_pct": "Annual Growth Rate (CAGR %)", "skill": "Skill"},
                color="growth_cagr_pct",
                color_continuous_scale="Reds_r"
            )
            fig_dec.update_layout(yaxis={'categoryorder': 'total descending'}, height=320)
            st.plotly_chart(fig_dec, use_container_width=True)

    st.markdown("---")
    st.subheader("Comprehensive 5-Year Market Demand Projections")
    all_forecasts = results.get("all_skill_forecasts", [])
    if all_forecasts:
        df_all = pd.DataFrame(all_forecasts)
        
        fig_trend = go.Figure()
        for _, row in df_all.head(8).iterrows():
            fig_trend.add_trace(go.Scatter(
                x=["2024 (Baseline)", "2025 (1-Yr)", "2026 (2-Yr)", "2029 (5-Yr)"],
                y=[row["freq_2024_actual"], row["projected_2025_demand"], row["projected_2026_demand"], row["projected_2029_demand"]],
                mode='lines+markers',
                name=row["skill"]
            ))
        fig_trend.update_layout(
            title="Projected Job Posting Volume Trajectory (Top Skills)",
            yaxis_title="Estimated Job Postings Frequency",
            height=380
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.dataframe(
            df_all[["skill", "domain", "growth_cagr_pct", "freq_2024_actual", "projected_2025_demand", "projected_2026_demand", "projected_2029_demand", "market_trajectory"]].rename(
                columns={
                    "skill": "Skill Name",
                    "domain": "Domain",
                    "growth_cagr_pct": "CAGR (%)",
                    "freq_2024_actual": "2024 Demand",
                    "projected_2025_demand": "2025 (1-Yr)",
                    "projected_2026_demand": "2026 (2-Yr)",
                    "projected_2029_demand": "2029 (5-Yr)",
                    "market_trajectory": "Status"
                }
            ),
            use_container_width=True
        )
