from typing import List, Dict, Any, Optional
import networkx as nx
from src.knowledge_graph.graph_engine import get_knowledge_graph
from src.semantic_matching.semantic_engine import get_semantic_matcher
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Curated high-impact learning resource templates for common skills
SKILL_RESOURCES = {
    "Python": {
        "title": "Mastering Modern Python for Data & AI",
        "type": "Interactive Course + Hands-on Labs",
        "est_hours": 20,
        "key_topics": ["Data Structures", "OOP", "Vectorization", "Async Programming"],
        "project": "Build an Automated Data Extraction Pipeline"
    },
    "SQL": {
        "title": "Advanced SQL & Analytical Window Functions",
        "type": "Case Study Workshop",
        "est_hours": 15,
        "key_topics": ["CTEs", "Window Partitions", "Query Optimization", "Database Indexing"],
        "project": "Complex Multi-Source Cohort Retention Analysis"
    },
    "Pandas": {
        "title": "High-Performance Data Wrangling with Pandas",
        "type": "Code-along Tutorial",
        "est_hours": 15,
        "key_topics": ["MultiIndex", "Groupby Aggregations", "Memory Optimization", "TimeSeries"],
        "project": "Financial Market Tick Data Processor"
    },
    "Scikit-Learn": {
        "title": "Production Machine Learning with Scikit-Learn",
        "type": "End-to-End Course",
        "est_hours": 25,
        "key_topics": ["Pipeline Orchestration", "Cross-Validation", "Ensemble Modeling", "Hyperopt"],
        "project": "Predictive Customer Churn Classifier with Feature Importance"
    },
    "TensorFlow": {
        "title": "Deep Learning Architecture with TensorFlow 2.x & Keras",
        "type": "Specialization",
        "est_hours": 30,
        "key_topics": ["CNNs", "RNN/LSTM", "Custom Layers", "TF.data pipelines"],
        "project": "Computer Vision Defect Detection Model"
    },
    "PyTorch": {
        "title": "Deep Learning & Neural Networks with PyTorch",
        "type": "Research to Production Course",
        "est_hours": 30,
        "key_topics": ["Autograd", "TorchVision", "Custom Training Loops", "DDP Distributed Training"],
        "project": "Multi-Modal Sentiment Classifier"
    },
    "Docker": {
        "title": "Containerization & Microservices with Docker",
        "type": "Practical DevOps Lab",
        "est_hours": 12,
        "key_topics": ["Dockerfile Optimization", "Multi-stage Builds", "Compose", "Networking"],
        "project": "Containerize a FastAPI ML Prediction Service"
    },
    "MLOps": {
        "title": "End-to-End MLOps: CI/CD, MLflow & Deployment",
        "type": "Engineering Masterclass",
        "est_hours": 25,
        "key_topics": ["Model Registry", "Drift Monitoring", "Feature Stores", "Automated Retraining"],
        "project": "Full Production ML Pipeline with Drift Alarms"
    },
    "FastAPI": {
        "title": "High-Throughput ML API Development with FastAPI",
        "type": "Crash Course",
        "est_hours": 12,
        "key_topics": ["Pydantic v2", "Async Endpoints", "Swagger UI", "Rate Limiting"],
        "project": "Real-time Recommendation API with Sub-10ms Latency"
    },
    "XGBoost": {
        "title": "Gradient Boosted Decision Trees in Production",
        "type": "Algorithmic Deep Dive",
        "est_hours": 15,
        "key_topics": ["Tree Pruning", "Early Stopping", "Categorical Encoders", "SHAP Explainability"],
        "project": "Credit Risk Default Prediction Engine"
    },
    "Transformers": {
        "title": "HuggingFace Transformers & Modern LLM Architectures",
        "type": "Applied GenAI Lab",
        "est_hours": 30,
        "key_topics": ["Attention Mechanisms", "Fine-Tuning PEFT/LoRA", "Quantization", "Tokenization"],
        "project": "Domain-Specific Legal Document Summarizer"
    },
    "LLMs": {
        "title": "Building GenAI Agents & RAG Applications",
        "type": "Applied AI Bootcamp",
        "est_hours": 25,
        "key_topics": ["Vector Embeddings", "Prompt Engineering", "Evaluation Frameworks", "LangChain/LlamaIndex"],
        "project": "Enterprise RAG Q&A System with Citations"
    },
    "Tableau": {
        "title": "Interactive Executive Dashboards in Tableau",
        "type": "Visual Analytics Studio",
        "est_hours": 15,
        "key_topics": ["LOD Expressions", "Interactive Actions", "Parameter Controls", "Storytelling"],
        "project": "C-Suite Global Revenue Cockpit"
    },
    "Power BI": {
        "title": "Enterprise Analytics with Microsoft Power BI & DAX",
        "type": "Hands-on Masterclass",
        "est_hours": 18,
        "key_topics": ["DAX Measures", "Power Query ETL", "Data Modeling", "Row-Level Security"],
        "project": "Supply Chain Efficiency Analytics Hub"
    }
}

class PersonalizedRoadmapEngine:
    """
    AI-Powered Learning Recommendation Engine
    Sequences personalized week-by-week curriculum based on Knowledge Graph dependencies,
    industry demand, and candidate skill gaps.
    """
    def __init__(self):
        self.kg = get_knowledge_graph()
        self.matcher = get_semantic_matcher()

    def generate_roadmap(
        self,
        candidate_skills: List[str],
        target_role: str,
        target_role_skills: List[str],
        hours_per_week: int = 10
    ) -> Dict[str, Any]:
        """
        Generates structured, time-phased learning roadmap.
        Returns:
            - current_readiness_pct: float
            - missing_skills: List[str]
            - hidden_blocker_skills: List[str]
            - roadmap_phases: List of weekly learning chunks
            - total_estimated_weeks: int
            - projected_readiness_trajectory: List of progress checkpoints
        """
        cand_lower = {s.strip().lower() for s in candidate_skills if s.strip()}
        
        # 1. Semantic match to find missing required skills
        match_res = self.matcher.match_skills(candidate_skills, target_role_skills)
        missing_skills = [m["skill"] for m in match_res["missing_skills"]]
        matched_skills = [m["required_skill"] for m in match_res["matched_skills"]]

        # 2. Hidden prerequisite gap detection
        hidden_gaps = self.kg.detect_hidden_skill_gaps(candidate_skills, missing_skills)
        hidden_blocker_names = [h["skill"] for h in hidden_gaps]

        # Combine all skills to learn (blockers first, then missing target skills)
        all_skills_to_learn = list(dict.fromkeys(hidden_blocker_names + missing_skills))

        if not all_skills_to_learn:
            return {
                "current_readiness_pct": 100.0,
                "target_role": target_role,
                "status": "Candidate exceeds all skill requirements for this role!",
                "missing_skills": [],
                "roadmap_phases": [],
                "total_estimated_weeks": 0,
                "projected_trajectory": []
            }

        # 3. Order skills topologically using the Knowledge Graph
        ordered_skills = self._topological_skill_sort(all_skills_to_learn)

        # 4. Partition into 2-week curriculum sprints
        roadmap_phases = []
        current_week = 1
        initial_readiness = match_res["match_rate_pct"]
        running_readiness = initial_readiness
        trajectory = [{"week": 0, "readiness_pct": round(initial_readiness, 1), "milestone": "Current Baseline"}]

        # Allocate approx 1-2 skills per 2-week block
        step = 0
        while step < len(ordered_skills):
            chunk = ordered_skills[step:step+2]
            duration_weeks = 2 if len(chunk) > 1 else 1
            week_label = f"Week {current_week}-{current_week + duration_weeks - 1}" if duration_weeks > 1 else f"Week {current_week}"
            
            phase_skills = []
            phase_hours = 0
            for skill_name in chunk:
                # Get or construct resource details
                res_info = SKILL_RESOURCES.get(skill_name, {
                    "title": f"Applied {skill_name} Mastery & Case Studies",
                    "type": "Comprehensive Module & Hands-on Lab",
                    "est_hours": 15,
                    "key_topics": [f"{skill_name} Fundamentals", "Real-world Implementations", "Best Practices", "Testing"],
                    "project": f"End-to-End {skill_name} Capstone Challenge"
                })
                
                phase_skills.append({
                    "skill": skill_name,
                    "module_title": res_info["title"],
                    "learning_format": res_info["type"],
                    "estimated_hours": res_info["est_hours"],
                    "key_topics": res_info["key_topics"],
                    "capstone_project": res_info["project"]
                })
                phase_hours += res_info["est_hours"]

            # Compute readiness gain for this sprint
            gain_per_skill = (100.0 - initial_readiness) / max(1, len(ordered_skills))
            running_readiness = min(100.0, running_readiness + (gain_per_skill * len(chunk)))

            roadmap_phases.append({
                "phase_index": len(roadmap_phases) + 1,
                "timeframe": week_label,
                "skills_covered": [s["skill"] for s in phase_skills],
                "modules": phase_skills,
                "total_phase_hours": phase_hours,
                "estimated_completion_weeks": duration_weeks,
                "projected_readiness_after_phase": round(running_readiness, 1)
            })

            current_week += duration_weeks
            trajectory.append({
                "week": current_week - 1,
                "readiness_pct": round(running_readiness, 1),
                "milestone": f"Completed {', '.join([s['skill'] for s in phase_skills])}"
            })
            step += 2

        total_weeks = current_week - 1

        return {
            "target_role": target_role,
            "current_readiness_pct": round(initial_readiness, 1),
            "projected_final_readiness_pct": 100.0,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "hidden_prerequisite_blockers": hidden_blocker_names,
            "total_skills_to_acquire": len(ordered_skills),
            "total_estimated_weeks": total_weeks,
            "total_learning_hours": sum(p["total_phase_hours"] for p in roadmap_phases),
            "roadmap_phases": roadmap_phases,
            "projected_trajectory": trajectory
        }

    def _topological_skill_sort(self, skills: List[str]) -> List[str]:
        """Sorts skill list respecting DAG dependencies in Knowledge Graph with industry demand fallback."""
        sub_nodes = set(self.kg.graph.nodes)
        valid_skills = [s for s in skills if s in sub_nodes]
        unmapped = [s for s in skills if s not in sub_nodes]

        if not valid_skills:
            return skills

        # Create induced subgraph
        subgraph = self.kg.graph.subgraph(valid_skills).copy()
        
        try:
            # Topological sort
            sorted_valid = list(nx.topological_sort(subgraph))
        except Exception:
            # If cycle or disjoint, sort by difficulty ascending, demand descending
            sorted_valid = sorted(
                valid_skills,
                key=lambda x: (self.kg.graph.nodes[x].get("difficulty", 2), -self.kg.graph.nodes[x].get("demand", 80))
            )

        return sorted_valid + unmapped

# Global singleton
_roadmap_instance = None

def get_roadmap_engine() -> PersonalizedRoadmapEngine:
    global _roadmap_instance
    if _roadmap_instance is None:
        _roadmap_instance = PersonalizedRoadmapEngine()
    return _roadmap_instance
