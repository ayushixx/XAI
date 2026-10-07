# 8BIT Workforce Signal Engine & AI Talent Intelligence Suite v2.0

Enterprise-grade AI Skill Gap Analysis, Knowledge Graph Discovery, Semantic Matching, Hybrid Weighted Evaluation Fusion (HWEF), and Personalized Learning Roadmap Platform.

---

## 🌟 Key Architecture & Pillars

### 1. Hybrid Weighted Evaluation Fusion (HWEF)
- Multimodal evaluation combining 5 calibrated signals into an overall **Job Fit Score**, **Skill Gap %**, and **Candidate Ranking Score**:
  - `skill_match` (40%) - Sentence-BERT semantic similarity
  - `experience` (25%) - Calibrated non-linear experience saturation
  - `projects` (15%) - Technical complexity & domain alignment
  - `certifications` (10%) - Tiered accreditation weighting
  - `ml_prediction` (10%) - ML predictive prior
- Configurable via `src/config/weights.json` and editable via Admin UI / API (`/api/hwef/weights`).

### 2. Semantic Skill Matching
- Powered by `sentence-transformers` (`all-MiniLM-L6-v2`) with embedding disk caching (`data/cache/`).
- Resolves domain synonyms (e.g. *ML ≈ Machine Learning*, *DL ≈ Neural Networks*, *Tableau ≈ Power BI*).
- Outputs: Match Rate %, Matched Skills with similarity badges, Missing Skills, and Synergistic Related Skills.

### 3. Skill Knowledge Graph (NetworkX Engine)
- Directed Acyclic Graph (DAG) modeling 40+ skills, prerequisite relationships, domain categories, difficulty tiers, and market demand indices.
- **Hidden Skill Gap Detection**: Automatically detects root prerequisite blockers (e.g., candidate lacking Python/NumPy before learning TensorFlow).
- **Career Path Trajectory**: Finds shortest, optimal learning progression from any start skill to target destination.

### 4. Personalized AI Learning Roadmap Engine
- AI-driven week-by-week curriculum generator (e.g. Week 1-2, Week 3-4, Week 5-6, Week 7, Week 8).
- Sequences skills topologically respecting prerequisite dependencies.
- Assigns capstone project milestones, estimated study hours, and projected readiness leap.

### 5. Explainable AI (XAI) & Attribution
- Dedicated explainability dashboard displaying:
  - 6-Dimensional Radar Chart
  - Skill Gap Heatmap
  - HWEF Signal Feature Attribution
  - Calibrated Readiness Gauge & Confidence score

### 6. Future Skill Demand Prediction
- XGBoost workforce analytics forecaster modeling 2-5 year market trajectories.
- Identifies **Hyper-Growth Emerging Technologies** (GenAI, LLMs, RAG, Vector DBs) vs **Declining Technologies** (Legacy SAS, VBA, Hadoop MapReduce).

### 7. Advanced Machine Learning Suite
- Integrates **XGBoost**, **LightGBM**, and **CatBoost** alongside **Random Forest**, **Decision Tree**, and **Logistic Regression**.
- Serialized models stored in `models/advanced/`.

### 8. Enhanced Evaluation Metrics
- Accuracy, ROC-AUC, F1 Score, Precision, Recall, Balanced Accuracy, Brier Calibration Score, and Confusion Matrix.
- Automated report generation in Markdown, CSV, and JSON (`reports/models/`).

### 9. Presentation-Ready Interactive Multi-Page Web Dashboard
- 6 Dedicated views:
  1. Skill Gap Dashboard
  2. Candidate Analysis & XAI
  3. Skill Knowledge Graph (Interactive Canvas with Vis.js)
  4. Personalized Learning Roadmap
  5. Future Skills Demand & Forecasting
  6. Recruiter Analytics & Live Weights Configurator
  7. ML Model CV Benchmarks

---

## 🚀 How to Run

### 1. Execute End-to-End Pipeline
```bash
python run_pipeline.py
```
*Runs data inventory, cleaning, EDA, statistics, baseline models, SAS signal engine, advanced gradient boosting, Knowledge Graph generation, and future demand forecasting.*

### 2. Launch FastAPI REST Server & Interactive Dashboard
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```
Open **`http://localhost:8000`** or **`http://localhost:8000/docs`** for interactive Swagger API docs.

