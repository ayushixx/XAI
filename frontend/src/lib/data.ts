import { CandidateProfile, SkillNode, FutureSkillDemand, AlgorithmCard, SHAPContribution, CounterfactualRec } from "./types";

export const DEFAULT_CANDIDATE: CandidateProfile = {
  id: "CAND-8BIT-001",
  name: "Alex Chen",
  currentRole: "Data Analyst / Junior ML Engineer",
  targetRole: "AI & Generative AI Architect",
  yearsExperience: 3.5,
  skills: ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Git"],
  personalityTraits: {
    conscientiousness: 8.4,
    openness: 8.8,
    extraversion: 7.2,
    agreeableness: 7.6,
    neuroticism: 3.2
  },
  metrics: {
    workforceReadinessScore: 84.8,
    jobFitScore: 74.0,
    skillGapPercentage: 26.0,
    careerAlignmentScore: 88.5,
    successProbability: 86.2
  }
};

export const SKILL_NODES: SkillNode[] = [
  { id: "python", label: "Python", category: "Languages", pageRank: 0.142, degreeCentrality: 18, difficulty: "Foundational", estimatedWeeks: 4, prerequisites: [], historicalGrowthCAGR: 18.2 },
  { id: "sql", label: "SQL", category: "Databases", pageRank: 0.128, degreeCentrality: 16, difficulty: "Foundational", estimatedWeeks: 3, prerequisites: [], historicalGrowthCAGR: 15.0 },
  { id: "pandas", label: "Pandas", category: "Data & ML", pageRank: 0.088, degreeCentrality: 12, difficulty: "Foundational", estimatedWeeks: 2, prerequisites: ["python"], historicalGrowthCAGR: 12.4 },
  { id: "numpy", label: "NumPy", category: "Data & ML", pageRank: 0.082, degreeCentrality: 11, difficulty: "Foundational", estimatedWeeks: 2, prerequisites: ["python"], historicalGrowthCAGR: 11.0 },
  { id: "scikit-learn", label: "Scikit-Learn", category: "Data & ML", pageRank: 0.095, degreeCentrality: 14, difficulty: "Intermediate", estimatedWeeks: 4, prerequisites: ["pandas", "numpy"], historicalGrowthCAGR: 9.8 },
  { id: "docker", label: "Docker & Containers", category: "Cloud & DevOps", pageRank: 0.092, degreeCentrality: 15, difficulty: "Intermediate", estimatedWeeks: 3, prerequisites: [], historicalGrowthCAGR: 21.0 },
  { id: "fastapi", label: "FastAPI", category: "Languages", pageRank: 0.076, degreeCentrality: 10, difficulty: "Intermediate", estimatedWeeks: 3, prerequisites: ["python"], historicalGrowthCAGR: 29.5 },
  { id: "pytorch", label: "PyTorch", category: "Data & ML", pageRank: 0.114, degreeCentrality: 16, difficulty: "Advanced", estimatedWeeks: 6, prerequisites: ["scikit-learn"], historicalGrowthCAGR: 34.8 },
  { id: "tensorflow", label: "TensorFlow", category: "Data & ML", pageRank: 0.079, degreeCentrality: 13, difficulty: "Advanced", estimatedWeeks: 6, prerequisites: ["scikit-learn"], historicalGrowthCAGR: 14.5 },
  { id: "transformers", label: "Transformers", category: "AI & GenAI", pageRank: 0.098, degreeCentrality: 14, difficulty: "Advanced", estimatedWeeks: 5, prerequisites: ["pytorch"], historicalGrowthCAGR: 42.0 },
  { id: "rag", label: "RAG Architectures", category: "AI & GenAI", pageRank: 0.105, degreeCentrality: 15, difficulty: "Expert", estimatedWeeks: 4, prerequisites: ["transformers", "fastapi"], historicalGrowthCAGR: 64.1 },
  { id: "vector-dbs", label: "Vector DBs (Chroma/Pinecone)", category: "Databases", pageRank: 0.086, degreeCentrality: 12, difficulty: "Intermediate", estimatedWeeks: 3, prerequisites: ["sql"], historicalGrowthCAGR: 58.6 },
  { id: "mlops", label: "MLOps & CI/CD", category: "Cloud & DevOps", pageRank: 0.094, degreeCentrality: 14, difficulty: "Advanced", estimatedWeeks: 5, prerequisites: ["docker", "fastapi"], historicalGrowthCAGR: 38.5 },
  { id: "kubernetes", label: "Kubernetes", category: "Cloud & DevOps", pageRank: 0.081, degreeCentrality: 11, difficulty: "Expert", estimatedWeeks: 5, prerequisites: ["docker"], historicalGrowthCAGR: 22.5 }
];

export const SKILL_GRAPH_EDGES = [
  { source: "python", target: "pandas", label: "prerequisite" },
  { source: "python", target: "numpy", label: "prerequisite" },
  { source: "python", target: "fastapi", label: "prerequisite" },
  { source: "pandas", target: "scikit-learn", label: "prerequisite" },
  { source: "numpy", target: "scikit-learn", label: "prerequisite" },
  { source: "scikit-learn", target: "pytorch", label: "prerequisite" },
  { source: "scikit-learn", target: "tensorflow", label: "prerequisite" },
  { source: "pytorch", target: "transformers", label: "prerequisite" },
  { source: "transformers", target: "rag", label: "prerequisite" },
  { source: "fastapi", target: "rag", label: "prerequisite" },
  { source: "sql", target: "vector-dbs", label: "prerequisite" },
  { source: "vector-dbs", target: "rag", label: "prerequisite" },
  { source: "docker", target: "mlops", label: "prerequisite" },
  { source: "fastapi", target: "mlops", label: "prerequisite" },
  { source: "docker", target: "kubernetes", label: "prerequisite" }
];

export const DEFAULT_SHAP_CONTRIBUTIONS: SHAPContribution[] = [
  { feature: "AI & Machine Learning Competency", featureValue: 9.0, shapValue: 0.142, direction: "positive" },
  { feature: "Core Coding & Python Proficiency", featureValue: 8.5, shapValue: 0.118, direction: "positive" },
  { feature: "Mathematics & Statistical Foundations", featureValue: 8.0, shapValue: 0.075, direction: "positive" },
  { feature: "Dashboard & Executive Storytelling", featureValue: 6.5, shapValue: 0.024, direction: "positive" },
  { feature: "Big Data & Distributed Systems", featureValue: 4.0, shapValue: -0.062, direction: "negative" },
  { feature: "Missing Production Containerization (Docker)", featureValue: 0.0, shapValue: -0.078, direction: "negative" }
];

export const COUNTERFACTUAL_SKILLS: CounterfactualRec[] = [
  { skill: "Docker & Containerization", marginalGain: 9.5, counterfactualScore: 83.5, learningTimeWeeks: 3, roiIndex: 3.17, whyRecommended: "Resolves deployment deficit in Tree model", difficulty: "Intermediate" },
  { skill: "PyTorch & Deep Learning", marginalGain: 13.0, counterfactualScore: 87.0, learningTimeWeeks: 5, roiIndex: 2.60, whyRecommended: "Massive boost in high-dimensional feature split", difficulty: "Advanced" },
  { skill: "RAG Architectures & Vector DBs", marginalGain: 14.5, counterfactualScore: 88.5, learningTimeWeeks: 4, roiIndex: 3.63, whyRecommended: "Direct alignment with GenAI target requirements", difficulty: "Expert" },
  { skill: "MLOps & CI/CD Pipeline Automation", marginalGain: 7.0, counterfactualScore: 81.0, learningTimeWeeks: 4, roiIndex: 1.75, whyRecommended: "Completes production infrastructure branch", difficulty: "Advanced" },
  { skill: "FastAPI Backend AI Serving", marginalGain: 6.0, counterfactualScore: 80.0, learningTimeWeeks: 3, roiIndex: 2.00, whyRecommended: "Unlocks real-time inference microservice path", difficulty: "Intermediate" }
];

export const FUTURE_DEMAND_DATA: FutureSkillDemand[] = [
  { skill: "RAG Architectures", domain: "AI / GenAI", status: "Hyper-Growth", growthCAGR: 64.1, actualDemand2024: 2800, projectedDemand2025: 4595, projectedDemand2026: 7540, projectedDemand2029: 20300 },
  { skill: "Vector Databases", domain: "Data Infrastructure", status: "Hyper-Growth", growthCAGR: 58.6, actualDemand2024: 2400, projectedDemand2025: 3806, projectedDemand2026: 6037, projectedDemand2029: 15200 },
  { skill: "Generative AI & LLMs", domain: "AI / GenAI", status: "Hyper-Growth", growthCAGR: 52.4, actualDemand2024: 4200, projectedDemand2025: 6401, projectedDemand2026: 9755, projectedDemand2029: 22700 },
  { skill: "Transformers", domain: "Generative AI", status: "Hyper-Growth", growthCAGR: 42.0, actualDemand2024: 3600, projectedDemand2025: 5112, projectedDemand2026: 7259, projectedDemand2029: 14600 },
  { skill: "MLOps & Monitoring", domain: "DevOps / MLOps", status: "High Growth", growthCAGR: 38.5, actualDemand2024: 3900, projectedDemand2025: 5402, projectedDemand2026: 7481, projectedDemand2029: 14300 },
  { skill: "PyTorch", domain: "Deep Learning", status: "High Growth", growthCAGR: 34.8, actualDemand2024: 5100, projectedDemand2025: 6875, projectedDemand2026: 9267, projectedDemand2029: 16900 },
  { skill: "FastAPI", domain: "Backend / AI Serving", status: "High Growth", growthCAGR: 29.5, actualDemand2024: 4600, projectedDemand2025: 5957, projectedDemand2026: 7714, projectedDemand2029: 12900 },
  { skill: "Docker", domain: "Cloud & Containers", status: "High Growth", growthCAGR: 21.0, actualDemand2024: 6200, projectedDemand2025: 7502, projectedDemand2026: 9077, projectedDemand2029: 13200 },
  { skill: "Hadoop MapReduce", domain: "Legacy Big Data", status: "Declining", growthCAGR: -22.4, actualDemand2024: 1600, projectedDemand2025: 1242, projectedDemand2026: 963, projectedDemand2029: 450 },
  { skill: "SPSS Statistics", domain: "Legacy Stats", status: "Declining", growthCAGR: -24.0, actualDemand2024: 1100, projectedDemand2025: 836, projectedDemand2026: 635, projectedDemand2029: 280 },
  { skill: "Perl Scripting", domain: "Legacy Scripting", status: "Declining", growthCAGR: -31.8, actualDemand2024: 550, projectedDemand2025: 375, projectedDemand2026: 256, projectedDemand2029: 80 }
];

export const ALGORITHM_REGISTRY: AlgorithmCard[] = [
  {
    id: "sbert",
    name: "Sentence-BERT (SBERT)",
    category: "Semantic NLP",
    purpose: "Generates 384-dimensional dense semantic vector embeddings for skills and job requirements to capture conceptual synonyms beyond exact keywords.",
    formula: "\\text{Sim}_{\\cos}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2}",
    formulaExplanation: "Embeds texts into Siamese transformer vector space; Cosine similarity measures angular alignment between candidate skills and job requirements.",
    inputs: ["Raw Candidate Skills String Array", "Target Job Posting Skill Requirements"],
    outputs: ["384-d Embedding Vectors", "Cosine Similarity Matrix", "Semantic Match Score [0-100]"],
    keyMetric: "all-MiniLM-L6-v2 (384 Dimensions)",
    codeSnippet: "from sentence_transformers import SentenceTransformer\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\nemb1 = model.encode('ML')\nemb2 = model.encode('Machine Learning')\nsim = cosine_similarity(emb1, emb2) # 0.94"
  },
  {
    id: "hwef",
    name: "Harmonic Weighted Employability Function (HWEF)",
    category: "Optimization",
    purpose: "Harmonically averages technical capabilities, soft traits, and experience ratios to enforce balanced readiness and severely penalize critical single-point deficiencies.",
    formula: "\\text{HWEF} = \\frac{w_{\\text{tech}} + w_{\\text{soft}} + w_{\\text{exp}}}{\\frac{w_{\\text{tech}}}{S_{\\text{tech}} + \\epsilon} + \\frac{w_{\\text{soft}}}{S_{\\text{soft}} + \\epsilon} + \\frac{w_{\\text{exp}}}{E_{\\text{exp}} + \\epsilon}}",
    formulaExplanation: "Unlike arithmetic means where a 100% in coding masks a 0% in experience, the harmonic mean collapses if any core pillar is zero.",
    inputs: ["Technical Skill Match (0-100)", "Soft Trait Index (0-100)", "Experience Ratio (Years/Required)"],
    outputs: ["Calibrated Employability Score [0-100]", "Penalization Deficit Magnitude"],
    keyMetric: "Weights: 0.50 Tech / 0.30 Soft / 0.20 Exp",
    codeSnippet: "def hwef(tech, soft, exp):\n    denom = (0.5/tech) + (0.3/soft) + (0.2/exp)\n    return (1.0 / denom)"
  },
  {
    id: "shap",
    name: "SHAP (TreeExplainer)",
    category: "Explainability",
    purpose: "Axiomatically computes exact additive Shapley feature attributions from cooperative game theory to explain why a candidate received their specific match score.",
    formula: "\\phi_i(f, \\mathbf{x}) = \\sum_{S \\subseteq F \\setminus \\{i\\}} \\frac{|S|! (|F| - |S| - 1)!}{|F|!} [f_x(S \\cup \\{i\\}) - f_x(S)]",
    formulaExplanation: "Decomposes candidate prediction into sum of feature effects: f(x) = E[f(x)] + Σ φ_i.",
    inputs: ["Trained XGBoost / Tree Model", "Candidate Capability Vector (5 Features)"],
    outputs: ["Local Waterfall Attribution Vector", "Global Mean |SHAP| Feature Importance"],
    keyMetric: "Zero-error Additive Attribution",
    codeSnippet: "import shap\nexplainer = shap.TreeExplainer(model)\nshap_values = explainer.shap_values(candidate_features)"
  },
  {
    id: "dijkstra",
    name: "Dijkstra Shortest Path (Career GPS)",
    category: "Graph Theory",
    purpose: "Navigates the weighted skill dependency knowledge graph to discover the globally optimal, minimum-time sequence of skills to reach any destination career role.",
    formula: "\\text{dist}[v] = \\min_{(u, v) \\in E} (\\text{dist}[u] + w(u, v))",
    formulaExplanation: "Maintains a min-priority queue over graph edges weighted by learning weeks and cognitive difficulty.",
    inputs: ["Directed Skill Graph G=(V,E,w)", "Current Acquired Skill Set", "Target Destination Role"],
    outputs: ["Ordered Trajectory Milestones", "Total Path Cost & Duration", "Salary Growth Multipliers"],
    keyMetric: "O((V + E) log V) Min-Heap Complexity",
    codeSnippet: "import networkx as nx\npath = nx.dijkstra_path(G, source='Python', target='AI_Engineer', weight='weeks')"
  },
  {
    id: "counterfactual",
    name: "Counterfactual AI Engine",
    category: "Optimization",
    purpose: "Executes what-if simulations to calculate the exact marginal employability delta for hypothetical skill acquisitions and identifies optimal minimal bundles.",
    formula: "\\Delta \\text{Score}(s_k) = f(X \\cup \\{s_k\\}) - f(X)",
    formulaExplanation: "Tests perturbation of the candidate profile vector across missing skill candidates to determine optimal intervention.",
    inputs: ["Candidate Profile Vector X", "Missing Skill Set Candidates", "Scoring Function f(X)"],
    outputs: ["Marginal Gain Rankings (+Δ%)", "Optimal Minimal Upskilling Bundles", "ROI Rankings"],
    keyMetric: "ΔScore = f(X') - f(X)",
    codeSnippet: "for skill in missing:\n    score_prime = model.predict(skills + [skill])\n    gain = score_prime - baseline_score"
  },
  {
    id: "pagerank",
    name: "PageRank & Composite Centrality",
    category: "Graph Theory",
    purpose: "Evaluates the topological influence of skill nodes across the workforce knowledge graph to detect high-leverage anchor competencies.",
    formula: "\\mathbf{PR}(v_i) = \\frac{1-d}{|V|} + d \\sum_{v_j \\in \\mathcal{M}(v_i)} \\frac{\\mathbf{PR}(v_j)}{L(v_j)}",
    formulaExplanation: "Calculates steady-state probability distribution of navigating the skill prerequisite topology.",
    inputs: ["Skill Knowledge Graph Topology (38 Nodes, 40 Edges)"],
    outputs: ["PageRank Distribution", "In-Degree / Out-Degree", "Composite Centrality Index"],
    keyMetric: "Damping factor d = 0.85",
    codeSnippet: "pr = nx.pagerank(G, alpha=0.85)\ncentrality = 0.40*pr + 0.35*degree + 0.25*betweenness"
  },
  {
    id: "autoencoder",
    name: "Deep Personality Autoencoder",
    category: "Machine Learning",
    purpose: "Non-linear neural compression network mapping 5-dimensional Big-Five traits into a 3D latent personality manifold for behavioral clustering and digital twin simulation.",
    formula: "\\mathcal{L}_{AE} = \\frac{1}{N} \\sum_{i=1}^N \\|\\mathbf{x}_i - g_\\phi(f_\\theta(\\mathbf{x}_i))\\|_2^2",
    formulaExplanation: "Encoder: 5 → 16 → 8 → 3 (Latent z). Decoder: 3 → 8 → 16 → 5 (Reconstruction x̂).",
    inputs: ["OCEAN Personality Traits (5 Dimensions)"],
    outputs: ["Latent Coordinate Vector z ∈ ℝ³", "Reconstructed Trait Vector", "Digital Twin Delta"],
    keyMetric: "PyTorch 5-Layer Autoencoder",
    codeSnippet: "class Autoencoder(nn.Module):\n    def __init__(self):\n        self.encoder = nn.Sequential(nn.Linear(5,16), nn.Linear(16,8), nn.Linear(8,3))\n        self.decoder = nn.Sequential(nn.Linear(3,8), nn.Linear(8,16), nn.Linear(16,5))"
  },
  {
    id: "xgboost",
    name: "XGBoost Regressor (Demand Forecasting)",
    category: "Machine Learning",
    purpose: "Predicts future skill demand and posting frequencies over 1-year, 2-year, and 5-year horizons using second-order gradient boosted decision trees.",
    formula: "\\mathcal{L}^{(t)} \\approx \\sum_{i=1}^n [g_i f_t(\\mathbf{x}_i) + \\frac{1}{2} h_i f_t^2(\\mathbf{x}_i)] + \\Omega(f_t)",
    formulaExplanation: "Optimizes exact second-order Taylor expansion of the loss function with tree complexity regularization.",
    inputs: ["Macro Historical Demand Frequencies (2022-2024)", "CAGR Growth Rates", "Domain Features"],
    outputs: ["1-Yr (2025), 2-Yr (2026), 5-Yr (2029) Demand Forecasts", "Emerging vs Declining Classifications"],
    keyMetric: "Test R² = 0.6928",
    codeSnippet: "import xgboost as xgb\nmodel = xgb.XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.08)\nmodel.fit(X_train, y_train)"
  },
  {
    id: "wri",
    name: "Workforce Readiness Index (WRI)",
    category: "Optimization",
    purpose: "Behavioral psychology model translating Big Five traits into an actionable, normalized workplace readiness benchmark score.",
    formula: "\\text{WRI} = 0.30 \\cdot C + 0.25 \\cdot O + 0.20 \\cdot E + 0.15 \\cdot A - 0.10 \\cdot N",
    formulaExplanation: "Weights Conscientiousness (+30%), Openness (+25%), Extraversion (+20%), Agreeableness (+15%), with penalty for Neuroticism (-10%).",
    inputs: ["Big Five Trait Scores (0-10 or 0-100 scale)"],
    outputs: ["Workforce Readiness Score [0-100]", "Readiness Tier Classification", "Leadership Status"],
    keyMetric: "Validated Psychological Weighting",
    codeSnippet: "wri = 0.30*C + 0.25*O + 0.20*E + 0.15*A - 0.10*N\nnormalized_wri = np.clip(wri + 10.0, 0, 100)"
  },
  {
    id: "rag",
    name: "ChromaDB + SBERT RAG Retrieval",
    category: "GenAI & RAG",
    purpose: "Dense vector retrieval over ChromaDB containing authentic WEF, NASSCOM, and LinkedIn reports, feeding grounded context to LLM career advisors.",
    formula: "D^* = \\arg\\max_{d_j \\in \\mathcal{D}} \\text{Sim}_{\\cos}(\\mathbf{e}_q, \\mathbf{e}_{d_j})",
    formulaExplanation: "Performs HNSW approximate nearest neighbor search to inject factual labor market evidence into generation prompts.",
    inputs: ["User Career / Market Query", "ChromaDB Document Index (WEF, NASSCOM, LinkedIn)"],
    outputs: ["Retrieved Evidence Passages", "Source Citations", "Grounded Synthesis"],
    keyMetric: "Zero-Hallucination Policy Invariant",
    codeSnippet: "results = chroma_collection.query(query_texts=['2028 skills'], n_results=3)"
  }
];
