import streamlit as st
from src.services.llm_advisor import get_llm_advisor
from src.services.rag_service import get_rag_service
from src.counterfactual.counterfactual_engine import get_counterfactual_engine
from src.career_gps.career_gps_engine import get_career_gps_engine
from src.evaluation.workforce_index import get_workforce_index_engine
from src.services.shap_service import get_shap_service

def render_llm_advisor():
    st.title("LLM Career Advisor & Industry RAG System")
    st.markdown(
        "Executive AI Advisor grounded strictly in **Machine Learning, SHAP, and Graph Analytics**. "
        "The LLM **never calculates scores** — it synthesizes and explains deterministic ML results."
    )

    tab_adv, tab_rag = st.tabs(["AI Career Advisor", "ChromaDB Industry RAG Retrieval"])

    with tab_adv:
        col_in1, col_in2 = st.columns([1, 1])

        with col_in1:
            st.subheader("Candidate Information")
            name = st.text_input("Candidate Name:", value="Alex Chen")
            role = st.selectbox(
                "Target Role:",
                options=["AI Engineer", "MLOps Engineer", "Data Scientist", "Big Data Architect", "Generative AI Architect"]
            )
            provider = st.selectbox("LLM Provider Engine:", options=["auto (Gemini / OpenAI / Deterministic ML)", "gemini", "openai", "offline_ml"])
            
            cand_skills = st.multiselect(
                "Current Skills:",
                options=["Python", "SQL", "Pandas", "Scikit-Learn", "Docker", "FastAPI", "PyTorch", "MLOps"],
                default=["Python", "SQL", "Pandas", "Scikit-Learn"]
            )

        with col_in2:
            st.subheader("Personality Traits (OCEAN)")
            c = st.slider("Conscientiousness", 1.0, 10.0, 8.0, 0.5, key="adv_c")
            n = st.slider("Neuroticism", 1.0, 10.0, 3.5, 0.5, key="adv_n")
            o = st.slider("Openness", 1.0, 10.0, 8.5, 0.5, key="adv_o")
            e = st.slider("Extraversion", 1.0, 10.0, 7.0, 0.5, key="adv_e")
            a = st.slider("Agreeableness", 1.0, 10.0, 7.5, 0.5, key="adv_a")

        gen_btn = st.button("Generate Grounded Career Intelligence", type="primary")

        # Execute backend analytical engines
        cf_engine = get_counterfactual_engine()
        gps_engine = get_career_gps_engine()
        wri_engine = get_workforce_index_engine()
        shap_svc = get_shap_service()
        advisor = get_llm_advisor()

        cf_res = cf_engine.simulate_counterfactuals(candidate_skills=cand_skills, target_role=role)
        gps_res = gps_engine.navigate_career_path(current_skills=cand_skills, target_role=role)
        wri_res = wri_engine.compute_wri(conscientiousness=c, openness=o, extraversion=e, agreeableness=a, neuroticism=n)
        shap_res = shap_svc.explain_candidate(
            candidate_name=name,
            features={"coding_skills": 8.5, "ai_and_ml_skills": 8.0, "maths-stats_skills": 7.5, "big_data_skills": 7.0, "dashboard_and_storytelling_skills": 6.5},
            candidate_skills=cand_skills,
            missing_skills=cf_res.get("missing_skills", [])
        )

        intel = advisor.generate_career_intelligence(
            candidate_profile={"candidate_name": name, "target_role": role, "job_fit_score": cf_res["current_state"]["job_fit_score"], "skill_gap_percentage": cf_res["current_state"]["skill_gap_percentage"]},
            counterfactual_results=cf_res,
            career_gps_path=gps_res,
            wri_results=wri_res,
            shap_explanation=shap_res,
            provider=provider
        )

        st.markdown("---")
        st.subheader(f"Synthesized Career Strategy for {name}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Strategic Career Advice")
            st.info(intel.get("career_advice", ""))

            st.markdown("### Interview Preparation Focus")
            st.write(intel.get("interview_preparation", ""))

        with c2:
            st.markdown("### Actionable Learning Roadmap")
            st.write(intel.get("learning_roadmap", ""))

            st.markdown("### Market Salary Insights")
            st.success(intel.get("salary_insights", ""))

            st.markdown("### Career Risks & Vulnerabilities")
            st.warning(intel.get("career_risks", ""))

        st.caption(f"Zero-Hallucination Policy: Output verified and grounded by deterministic 8BIT ML engines. Source Provider: {intel.get('metadata', {}).get('llm_provider', 'ML Grounded')}")

    with tab_rag:
        st.subheader("ChromaDB Industry Knowledge Retrieval")
        st.markdown("Semantic search across **WEF Reports**, **NASSCOM Reports**, **LinkedIn Global Trends**, and **Future of Jobs Reports**.")

        rag_service = get_rag_service()

        query = st.text_input("Enter your industry inquiry:", value="What skills will be important in 2028?")
        rag_btn = st.button("Search Industry Knowledge Base", type="primary")

        ans = rag_service.answer_query(query)

        st.markdown("### Synthesized Executive Answer")
        st.write(ans.get("synthesized_answer", ""))

        st.markdown("### Retrieved Evidence Passages")
        for i, doc in enumerate(ans.get("retrieved_evidence", [])):
            with st.expander(f"Source: {doc.get('source', 'Report')} (Relevance: {doc.get('relevance_score', 0):.2f})"):
                st.write(doc.get("content", ""))
                st.caption(f"Domain: {doc.get('metadata', {}).get('domain', 'Tech')} | Year: {doc.get('metadata', {}).get('year', '2024')}")
