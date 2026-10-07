import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
from src.career_gps.career_gps_engine import get_career_gps_engine
from src.knowledge_graph.skill_graph import get_skill_graph

def render_career_gps():
    st.title("Career GPS & Skill Knowledge Graph")
    st.markdown(
        "Shortest-path algorithmic navigation over the **Workforce Knowledge Graph** using "
        "**Dijkstra's Algorithm** and **A\* Search** to discover the most efficient upskilling path."
    )

    gps_engine = get_career_gps_engine()
    skill_graph_engine = get_skill_graph()

    available_skills = [
        "Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Docker", "Kubernetes",
        "FastAPI", "TensorFlow", "PyTorch", "MLOps", "Transformers", "RAG Architectures",
        "Snowflake", "Databricks", "Tableau", "Power BI", "Git", "CI/CD", "Prompt Engineering"
    ]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Trajectory Parameters")
        current_skills = st.multiselect(
            "Current Acquired Skills:",
            options=available_skills,
            default=["Python", "SQL", "Pandas"]
        )
        target_role = st.selectbox(
            "Destination Career Role:",
            options=["AI Engineer", "MLOps Engineer", "Data Scientist", "Big Data Architect", "Generative AI Architect"]
        )
        algorithm = st.radio("Navigation Algorithm:", ["dijkstra", "astar"], horizontal=True)
        nav_btn = st.button("Calculate Optimal Trajectory", type="primary")

    nav_res = gps_engine.navigate_career_path(
        current_skills=current_skills,
        target_role=target_role,
        algorithm=algorithm
    )

    with col2:
        st.subheader("Route Summary")
        weeks = nav_res.get("estimated_learning_time_weeks", 0)
        cost = nav_res.get("path_length", 0)
        salary_growth = nav_res.get("expected_salary_growth_pct", "+85%")

        m1, m2, m3 = st.columns(3)
        m1.metric("Path Cost", f"{cost:.1f}")
        m2.metric("Est. Duration", f"{weeks} Weeks")
        m3.metric("Salary Upside", salary_growth)

        st.info(f"**Navigated Steps**: {' ➔ '.join(nav_res.get('trajectory_skills', []))}")

    st.markdown("---")

    tab1, tab2 = st.tabs(["Career Graph Navigation", "Skill Network & Centrality Graph"])

    with tab1:
        st.subheader("Milestone-by-Milestone Career Trajectory")
        trajectory = nav_res.get("gps_trajectory", [])
        if trajectory:
            df_traj = pd.DataFrame(trajectory)
            st.dataframe(
                df_traj[["step", "skill", "learning_weeks", "target_role", "salary_multiplier", "rationale"]].rename(
                    columns={
                        "step": "Step",
                        "skill": "Milestone Skill",
                        "learning_weeks": "Weeks Required",
                        "target_role": "Milestone Role",
                        "salary_multiplier": "Comp Multiplier",
                        "rationale": "Strategic Value"
                    }
                ),
                use_container_width=True
            )

            # Step line chart
            fig_steps = go.Figure()
            steps = [f"Step {s['step']}: {s['skill']}" for s in trajectory]
            cum_weeks = []
            running = 0
            for s in trajectory:
                running += s["learning_weeks"]
                cum_weeks.append(running)

            fig_steps.add_trace(go.Scatter(
                x=steps,
                y=cum_weeks,
                mode='lines+markers+text',
                text=[f"{w} wks" for w in cum_weeks],
                textposition="top center",
                line=dict(color='#D35400', width=3),
                marker=dict(size=12, color='#2980B9')
            ))
            fig_steps.update_layout(
                title="Cumulative Learning Time Across Milestone Progression",
                yaxis_title="Total Weeks",
                height=320
            )
            st.plotly_chart(fig_steps, use_container_width=True)

    with tab2:
        st.subheader("Global Skill Knowledge Graph & Centrality")
        critical_skills = skill_graph_engine.get_critical_skills(top_k=10)
        df_crit = pd.DataFrame(critical_skills)

        st.markdown("**Top Central Skills in the Workforce Knowledge Graph (Composite Centrality & PageRank)**")
        st.dataframe(
            df_crit[["skill", "composite_centrality", "pagerank", "degree", "in_degree", "out_degree"]].rename(
                columns={
                    "skill": "Skill Node",
                    "composite_centrality": "Composite Centrality",
                    "pagerank": "PageRank Score",
                    "degree": "Total Degree",
                    "in_degree": "Prerequisite For (Out)",
                    "out_degree": "Requires (In)"
                }
            ),
            use_container_width=True
        )

        # Draw Network Graph via NetworkX & Plotly
        G = skill_graph_engine.graph
        pos = nx.spring_layout(G, seed=42)

        edge_x = []
        edge_y = []
        for edge in G.edges():
            if edge[0] in pos and edge[1] in pos:
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.8, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        node_text = []
        node_color = []
        for node in G.nodes():
            if node in pos:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                degree = G.degree(node)
                node_text.append(f"Skill: {node}<br>Degree: {degree}")
                node_color.append(degree)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[node if G.degree(node) > 2 else "" for node in G.nodes()],
            textposition="top center",
            marker=dict(
                showscale=True,
                colorscale='YlOrRd',
                color=node_color,
                size=[max(12, min(30, G.degree(n) * 4)) for n in G.nodes()],
                colorbar=dict(
                    thickness=15,
                    title='Skill Connectivity',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=1
            )
        )

        fig_net = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='Interactive Workforce Skill Dependency Network',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=480
                     ))
        st.plotly_chart(fig_net, use_container_width=True)
