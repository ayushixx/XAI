# 8BIT Workforce Signal Engine & AI Talent Intelligence Suite v3.0

Enterprise-grade AI Skill Gap Analysis, Counterfactual Skill Optimization, Career GPS Navigation, Knowledge Graph Discovery, Semantic Matching (SBERT), Hybrid Weighted Evaluation Fusion (HWEF), and Explainable AI (SHAP / XAI) Platform.

---

## 🌟 Key Architecture & Pillars

### 1. Counterfactual Skill Recommendation Engine (What-If Optimization)
- **Mathematical Foundation**: Computes counterfactual explainability interventions:
  $$\Delta \text{Score} = f(X') - f(X)$$
  where $f(X)$ is the calibrated HWEF scoring engine on current state $X$, and $X' = X \cup \{S\}$ is the counterfactual state with injected skill $S$.
- **Minimal Skill Bundle Optimization**: Solves the combinatorial problem of finding the smallest skill set $S^* \subseteq \mathcal{U}_{\text{missing}}$ that maximizes employability while bounding learning friction using a greedy submodular optimization algorithm.
- **Multi-Skill Synergies**: Computes non-linear score interactions for paired and triplet skills (e.g. *TensorFlow + Docker* $\rightarrow$ 91% fit, +19% gain).
- **Explainability ("Why It Was Recommended")**:
  - Market Job Frequency % (percentage of target role postings demanding the skill)
  - Downstream Knowledge Graph Unlocks (number of reachable dependent skills)
  - Direct Job Fit Increase $\Delta f(X)$ %
  - Net Skill Gap Reduction %
- **REST API**: `POST /api/v2/counterfactual/simulate`

### 2. Career GPS (Knowledge Graph & Shortest Path Optimization)
- **Knowledge Graph Topology**: Directed Acyclic Graph (DAG) constructed in `NetworkX` comprising 40+ technology nodes across 12 specialized domains with prerequisite and unlock edges.
- **Edge Weight Friction Formula**:
  $$\text{Weight}(u, v) = 0.4 \cdot \text{LearningTime}(v) + 0.3 \cdot \text{Difficulty}(v) - 0.3 \cdot \text{MarketDemand}(v) + \text{Base}$$
  Normalized and bounded to ensure strictly positive edge friction for optimal graph traversal.
- **Pathfinding Algorithms**:
  - **Dijkstra's Shortest Path**: Globally minimizes cumulative friction score.
  - **A\* Heuristic Search**: Accelerates search using goal-distance and demand-potential heuristics:
    $$h(n) = \frac{\text{diff}(n, \text{goal}) + (100 - \text{demand}(n))}{100}$$
- **Projections & Milestones**:
  - Step-by-step milestone learning curriculum with domain badges and study hour breakdowns.
  - Cumulative study weeks and months based on candidate hours/week commitment.
  - Compound Salary Growth Projection % ($S_{\text{target}} / S_{\text{current}} - 1$) and benchmark compensation figures.
- **REST API**: `POST /api/v2/career-gps/navigate` and `GET /api/v2/career-gps/roles`

### 3. Hybrid Weighted Evaluation Fusion (HWEF)
- Multimodal evaluation combining 5 calibrated signals into an overall **Job Fit Score**, **Skill Gap %**, and **Candidate Ranking Score**:
  - `skill_match` (40%) - Sentence-BERT semantic similarity
  - `experience` (25%) - Calibrated non-linear experience saturation
  - `projects` (15%) - Technical complexity & domain alignment
  - `certifications` (10%) - Tiered accreditation weighting
  - `ml_prediction` (10%) - ML predictive prior
- Configurable via `src/config/weights.json` and editable via Admin UI / API (`/api/hwef/weights`).

### 4. Semantic Skill Matching (SBERT)
- Powered by `sentence-transformers` (`all-MiniLM-L6-v2`) with embedding disk caching (`data/cache/`).
- Resolves domain synonyms (e.g. *ML ≈ Machine Learning*, *DL ≈ Neural Networks*, *Tableau ≈ Power BI*).
- Outputs: Match Rate %, Matched Skills with similarity badges, Missing Skills, and Synergistic Related Skills.

### 5. Explainable AI (XAI) & Tree SHAP Attribution
- Integrated `shap.TreeExplainer` providing local additive feature attributions for candidate scores:
  $$f(x) = \mathbb{E}[f(x)] + \sum_{i=1}^{M} \phi_i$$
- 6-Dimensional Radar Chart, SHAP Waterfall/Bar visualizations, and calibrated confidence tiers.
- REST API: `POST /api/v2/xai/candidate/{candidate_id}`

### 6. Future Skill Demand Prediction
- XGBoost workforce analytics forecaster modeling 2-5 year market trajectories.
- Identifies **Hyper-Growth Emerging Technologies** (GenAI, LLMs, RAG, Vector DBs) vs **Declining Technologies** (Legacy SAS, VBA, Hadoop MapReduce).

### 7. Advanced Machine Learning Suite
- Integrates **XGBoost**, **LightGBM**, and **CatBoost** alongside **Random Forest**, **Decision Tree**, and **Logistic Regression**.
- Serialized models stored in `models/advanced/`.

### 8. Interactive Multi-Page Web Intelligence Suite
- 8 Dedicated interactive views:
  1. **Skill Gap Analysis & Semantic Matching**
  2. **Candidate Evaluation & Explainable AI (XAI / SHAP)**
  3. **Counterfactual Skill Recommendations & What-If Optimizer**
  4. **Career GPS Shortest Path Navigation (Dijkstra / A\*)**
  5. **NetworkX Skill Knowledge Graph Visualizer (Vis.js)**
  6. **Personalized AI Learning Roadmap**
  7. **Future Skill Demand Forecasting & Velocity**
  8. **Recruiter Talent Leaderboard & Live Weights Configurator**

---

## 🚀 How to Run

### 1. Execute End-to-End Pipeline
```bash
python run_pipeline.py
```
*Runs data inventory, cleaning, EDA, statistics, baseline models, SAS signal engine, advanced gradient boosting, Knowledge Graph generation, future demand forecasting, Counterfactual simulation, and Career GPS navigation.*

### 2. Launch FastAPI REST Server & Interactive Dashboard
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```
Open **`http://localhost:8000`** in your browser to access the complete interactive platform or **`http://localhost:8000/docs`** for interactive OpenAPI/Swagger documentation.

---

## 🧪 Mathematical Verification & Testing
To execute the test suite across all engines:
```bash
python -m unittest discover tests
```
*Verifies HWEF calibration, TreeExplainer SHAP attribution, Counterfactual marginal gains, Dijkstra/A\* Career GPS shortest path routing, and FastAPI router endpoints with 100% pass rate.*
