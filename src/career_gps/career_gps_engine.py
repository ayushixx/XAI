import math
from typing import List, Dict, Any, Optional, Set, Tuple
import networkx as nx
from src.knowledge_graph.graph_engine import get_knowledge_graph
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Standard career role definitions mapped to core target competencies
CAREER_TARGET_PROFILES = {
    "AI Engineer": {
        "title": "AI & Deep Learning Solutions Architect",
        "core_skills": ["Python", "NumPy", "Pandas", "Scikit-Learn", "Deep Learning", "TensorFlow", "PyTorch", "MLOps", "LLMs"],
        "baseline_salary_usd": 145000,
        "market_growth_pct": "+68%"
    },
    "Generative AI Architect": {
        "title": "Principal Generative AI & LLM Systems Engineer",
        "core_skills": ["Python", "PyTorch", "Deep Learning", "Transformers", "LLMs", "RAG Architectures", "Vector Databases", "Docker"],
        "baseline_salary_usd": 165000,
        "market_growth_pct": "+85%"
    },
    "MLOps Platform Engineer": {
        "title": "Production Machine Learning & Platform Engineer",
        "core_skills": ["Python", "SQL", "Scikit-Learn", "FastAPI", "Docker", "Kubernetes", "MLflow", "CI/CD", "Cloud Computing (AWS/GCP)"],
        "baseline_salary_usd": 140000,
        "market_growth_pct": "+52%"
    },
    "Senior Data Scientist": {
        "title": "Senior Data Scientist & Statistical Modeler",
        "core_skills": ["Python", "SQL", "Probability & Statistics", "Pandas", "Scikit-Learn", "Feature Engineering", "XGBoost", "Tableau"],
        "baseline_salary_usd": 135000,
        "market_growth_pct": "+35%"
    },
    "Data Engineer (Lakehouse)": {
        "title": "Big Data & Real-Time Lakehouse Architect",
        "core_skills": ["Python", "SQL", "Apache Spark", "PySpark", "Airflow", "Docker", "Cloud Computing (AWS/GCP)", "Data Cleaning"],
        "baseline_salary_usd": 130000,
        "market_growth_pct": "+42%"
    },
    "Lead BI & Analytics Translator": {
        "title": "Lead Business Intelligence & Analytics Translator",
        "core_skills": ["SQL", "Data Cleaning", "EDA", "Tableau", "Power BI", "Executive Storytelling", "Probability & Statistics"],
        "baseline_salary_usd": 115000,
        "market_growth_pct": "+25%"
    }
}

class CareerGPSEngine:
    """
    Career GPS Engine using Directed Weighted Knowledge Graph Optimization.
    Implements Dijkstra Shortest Path, A* Heuristic Search, and Multi-Node Traversal.
    Calculates the minimum learning friction path from current skillset to target career.
    """
    def __init__(self):
        self.kg = get_knowledge_graph()
        self.weighted_graph = nx.DiGraph()
        self._build_weighted_career_graph()

    def _build_weighted_career_graph(self):
        """
        Builds a comprehensive weighted knowledge graph incorporating:
        - Learning Difficulty (1-5 scale)
        - Learning Time (weeks required to master)
        - Market Demand (0-100 scale)
        - Incremental Salary Boost (% and $)
        
        Edge Weight Formula:
            Weight(u -> v) = 0.4 * (Learning Time) + 0.3 * (Difficulty) - 0.3 * (Normalized Market Demand) + Base Offset
        """
        # Node attributes
        node_catalog = {
            "Python": {"difficulty": 1, "weeks": 3, "demand": 98, "salary_boost_pct": 15.0, "domain": "Core Programming"},
            "SQL": {"difficulty": 1, "weeks": 2, "demand": 95, "salary_boost_pct": 12.0, "domain": "Data Management"},
            "Linear Algebra": {"difficulty": 2, "weeks": 3, "demand": 82, "salary_boost_pct": 8.0, "domain": "Math & Statistics"},
            "Calculus": {"difficulty": 2, "weeks": 3, "demand": 78, "salary_boost_pct": 6.0, "domain": "Math & Statistics"},
            "Probability & Statistics": {"difficulty": 2, "weeks": 3, "demand": 92, "salary_boost_pct": 12.0, "domain": "Math & Statistics"},
            
            "NumPy": {"difficulty": 2, "weeks": 2, "demand": 90, "salary_boost_pct": 8.0, "domain": "Data Engineering"},
            "Pandas": {"difficulty": 2, "weeks": 3, "demand": 94, "salary_boost_pct": 10.0, "domain": "Data Engineering"},
            "Data Cleaning": {"difficulty": 1, "weeks": 1, "demand": 88, "salary_boost_pct": 6.0, "domain": "Data Engineering"},
            "EDA": {"difficulty": 1, "weeks": 2, "demand": 89, "salary_boost_pct": 8.0, "domain": "Analytics"},
            "Feature Engineering": {"difficulty": 3, "weeks": 3, "demand": 89, "salary_boost_pct": 14.0, "domain": "Machine Learning"},
            
            "Matplotlib": {"difficulty": 2, "weeks": 1, "demand": 80, "salary_boost_pct": 4.0, "domain": "Visualization"},
            "Seaborn": {"difficulty": 2, "weeks": 1, "demand": 82, "salary_boost_pct": 5.0, "domain": "Visualization"},
            "Tableau": {"difficulty": 2, "weeks": 3, "demand": 86, "salary_boost_pct": 12.0, "domain": "Business Intelligence"},
            "Power BI": {"difficulty": 2, "weeks": 3, "demand": 89, "salary_boost_pct": 13.0, "domain": "Business Intelligence"},
            "Executive Storytelling": {"difficulty": 3, "weeks": 2, "demand": 85, "salary_boost_pct": 16.0, "domain": "Leadership"},
            
            "Scikit-Learn": {"difficulty": 3, "weeks": 4, "demand": 92, "salary_boost_pct": 16.0, "domain": "Machine Learning"},
            "Model Evaluation": {"difficulty": 2, "weeks": 2, "demand": 88, "salary_boost_pct": 10.0, "domain": "Machine Learning"},
            "XGBoost": {"difficulty": 3, "weeks": 2, "demand": 91, "salary_boost_pct": 15.0, "domain": "Machine Learning"},
            "LightGBM": {"difficulty": 3, "weeks": 2, "demand": 87, "salary_boost_pct": 14.0, "domain": "Machine Learning"},
            
            "Deep Learning": {"difficulty": 4, "weeks": 4, "demand": 93, "salary_boost_pct": 22.0, "domain": "Artificial Intelligence"},
            "TensorFlow": {"difficulty": 4, "weeks": 4, "demand": 88, "salary_boost_pct": 20.0, "domain": "Artificial Intelligence"},
            "PyTorch": {"difficulty": 4, "weeks": 4, "demand": 95, "salary_boost_pct": 24.0, "domain": "Artificial Intelligence"},
            "Computer Vision": {"difficulty": 4, "weeks": 4, "demand": 84, "salary_boost_pct": 18.0, "domain": "Specialized AI"},
            "NLP": {"difficulty": 4, "weeks": 4, "demand": 94, "salary_boost_pct": 22.0, "domain": "Specialized AI"},
            
            "Transformers": {"difficulty": 5, "weeks": 4, "demand": 97, "salary_boost_pct": 28.0, "domain": "Generative AI"},
            "LLMs": {"difficulty": 5, "weeks": 4, "demand": 99, "salary_boost_pct": 32.0, "domain": "Generative AI"},
            "RAG Architectures": {"difficulty": 4, "weeks": 3, "demand": 96, "salary_boost_pct": 25.0, "domain": "Generative AI"},
            "Vector Databases": {"difficulty": 3, "weeks": 2, "demand": 94, "salary_boost_pct": 20.0, "domain": "Generative AI"},
            
            "Git": {"difficulty": 1, "weeks": 1, "demand": 95, "salary_boost_pct": 5.0, "domain": "Software Engineering"},
            "FastAPI": {"difficulty": 2, "weeks": 2, "demand": 89, "salary_boost_pct": 14.0, "domain": "Backend"},
            "Docker": {"difficulty": 3, "weeks": 2, "demand": 93, "salary_boost_pct": 16.0, "domain": "Cloud & DevOps"},
            "Kubernetes": {"difficulty": 4, "weeks": 4, "demand": 88, "salary_boost_pct": 20.0, "domain": "Cloud & DevOps"},
            "CI/CD": {"difficulty": 3, "weeks": 2, "demand": 87, "salary_boost_pct": 12.0, "domain": "Cloud & DevOps"},
            "MLOps": {"difficulty": 4, "weeks": 4, "demand": 92, "salary_boost_pct": 24.0, "domain": "MLOps"},
            "LLMOps": {"difficulty": 5, "weeks": 3, "demand": 96, "salary_boost_pct": 28.0, "domain": "MLOps"},
            "MLflow": {"difficulty": 3, "weeks": 2, "demand": 90, "salary_boost_pct": 15.0, "domain": "MLOps"},
            "Cloud Computing (AWS/GCP)": {"difficulty": 3, "weeks": 4, "demand": 94, "salary_boost_pct": 18.0, "domain": "Cloud"},
            "Apache Spark": {"difficulty": 4, "weeks": 4, "demand": 89, "salary_boost_pct": 18.0, "domain": "Big Data"},
            "PySpark": {"difficulty": 3, "weeks": 3, "demand": 88, "salary_boost_pct": 17.0, "domain": "Big Data"},
            "Airflow": {"difficulty": 3, "weeks": 2, "demand": 86, "salary_boost_pct": 15.0, "domain": "Data Engineering"}
        }

        for node_id, attrs in node_catalog.items():
            self.weighted_graph.add_node(node_id, **attrs)

        # Directed Edges (u -> v represents u unlocks or is prerequisite of v)
        prerequisites = [
            ("Python", "NumPy"),
            ("Python", "Pandas"),
            ("Python", "FastAPI"),
            ("Python", "Git"),
            ("Linear Algebra", "NumPy"),
            ("Linear Algebra", "Deep Learning"),
            ("Calculus", "Deep Learning"),
            ("Probability & Statistics", "Scikit-Learn"),
            ("Probability & Statistics", "EDA"),
            ("NumPy", "Pandas"),
            ("NumPy", "Scikit-Learn"),
            ("Pandas", "Matplotlib"),
            ("Pandas", "Seaborn"),
            ("Pandas", "Feature Engineering"),
            ("Data Cleaning", "EDA"),
            ("EDA", "Feature Engineering"),
            ("SQL", "Data Cleaning"),
            ("SQL", "Tableau"),
            ("SQL", "Power BI"),
            ("SQL", "Apache Spark"),
            ("Tableau", "Executive Storytelling"),
            ("Power BI", "Executive Storytelling"),
            ("Scikit-Learn", "XGBoost"),
            ("Scikit-Learn", "LightGBM"),
            ("Scikit-Learn", "Deep Learning"),
            ("Scikit-Learn", "Model Evaluation"),
            ("Scikit-Learn", "MLOps"),
            ("Deep Learning", "PyTorch"),
            ("Deep Learning", "TensorFlow"),
            ("Deep Learning", "NLP"),
            ("Deep Learning", "Computer Vision"),
            ("PyTorch", "Transformers"),
            ("TensorFlow", "Transformers"),
            ("Transformers", "LLMs"),
            ("Transformers", "RAG Architectures"),
            ("LLMs", "LLMOps"),
            ("RAG Architectures", "Vector Databases"),
            ("Git", "CI/CD"),
            ("Docker", "Kubernetes"),
            ("Docker", "MLOps"),
            ("FastAPI", "MLOps"),
            ("MLOps", "LLMOps"),
            ("Cloud Computing (AWS/GCP)", "Kubernetes"),
            ("Cloud Computing (AWS/GCP)", "MLOps"),
            ("Apache Spark", "PySpark"),
            ("Python", "PySpark")
        ]

        for u, v in prerequisites:
            if u in self.weighted_graph and v in self.weighted_graph:
                v_attrs = self.weighted_graph.nodes[v]
                time_w = float(v_attrs.get("weeks", 2))
                diff_w = float(v_attrs.get("difficulty", 2))
                demand_w = float(v_attrs.get("demand", 80))

                # Edge cost represents learning friction: high time & difficulty increase cost; high market demand reduces resistance
                edge_cost = max(
                    0.1,
                    round(0.4 * (time_w / 3.0) + 0.3 * (diff_w / 3.0) - 0.3 * (demand_w / 100.0) + 0.4, 3)
                )
                self.weighted_graph.add_edge(u, v, weight=edge_cost, transition_weeks=time_w)

        logger.info(f"Career GPS Weighted Graph built with {self.weighted_graph.number_of_nodes()} nodes and {self.weighted_graph.number_of_edges()} edges.")

    def navigate_career_path(
        self,
        current_skills: List[str],
        target_role: str = "AI Engineer",
        algorithm: str = "dijkstra"
    ) -> Dict[str, Any]:
        """
        Executes optimal shortest path navigation from current skillset to target role.
        Utilizes Dijkstra or A* search to minimize total learning friction and time.
        """
        clean_cand = [s.strip() for s in current_skills if s.strip()]
        cand_set_lower = {s.lower() for s in clean_cand}

        # Resolve target role profile
        role_meta = CAREER_TARGET_PROFILES.get(target_role, {
            "title": target_role,
            "core_skills": ["Python", "SQL", "Pandas", "Scikit-Learn", "Deep Learning", "TensorFlow", "MLOps"],
            "baseline_salary_usd": 130000,
            "market_growth_pct": "+50%"
        })

        target_skills = role_meta["core_skills"]
        missing_target_skills = [t for t in target_skills if t.lower() not in cand_set_lower]

        if not missing_target_skills:
            return {
                "status": "Target Reached",
                "current_role": "Current Profile",
                "target_role": target_role,
                "path_length": 0,
                "gps_trajectory": [],
                "estimated_learning_time_weeks": 0,
                "estimated_learning_time_months": 0.0,
                "expected_salary_growth_pct": "+0%",
                "message": f"Candidate already possesses all core competencies for {target_role}!"
            }

        # Select anchor entry node in current skills
        entry_node = None
        for cand in clean_cand:
            for n in self.weighted_graph.nodes:
                if n.lower() == cand.lower():
                    entry_node = n
                    break
            if entry_node:
                break

        if not entry_node:
            entry_node = "Python"

        # Determine terminal destination node in target skills (usually the apex/most advanced skill)
        terminal_node = missing_target_skills[-1]
        if terminal_node not in self.weighted_graph:
            terminal_node = "Deep Learning" if "Deep Learning" in self.weighted_graph else list(self.weighted_graph.nodes)[0]

        # 1. Path Calculation (Dijkstra or A*)
        try:
            if algorithm.lower() == "astar":
                # Admissible heuristic: estimated remaining steps * min edge weight
                def heuristic(u, v):
                    return 0.2

                path = nx.astar_path(self.weighted_graph, entry_node, terminal_node, heuristic=heuristic, weight='weight')
            else:
                path = nx.dijkstra_path(self.weighted_graph, entry_node, terminal_node, weight='weight')
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # Ancestor fallback sequence
            ancestors = nx.ancestors(self.weighted_graph, terminal_node)
            path = [entry_node] + [a for a in ancestors if a.lower() not in cand_set_lower] + [terminal_node]
            path = list(dict.fromkeys(path))

        # Filter out skills candidate already has, while keeping chronological progression
        gps_steps = []
        cumulative_weeks = 0
        cumulative_salary_boost = 0.0
        running_salary = 75000  # Baseline current market salary

        for idx, skill in enumerate(path):
            is_already_acquired = skill.lower() in cand_set_lower
            node_attrs = self.weighted_graph.nodes.get(skill, {
                "difficulty": 2, "weeks": 2, "demand": 85, "salary_boost_pct": 10.0, "domain": "General"
            })

            step_weeks = 0 if is_already_acquired else node_attrs.get("weeks", 2)
            step_boost = 0.0 if is_already_acquired else node_attrs.get("salary_boost_pct", 10.0)

            cumulative_weeks += step_weeks
            cumulative_salary_boost += step_boost
            running_salary = running_salary * (1 + (step_boost / 100.0))

            deps = self.kg.get_skill_dependencies(skill)
            unlocks = deps.get("unlocks_skills", [])

            gps_steps.append({
                "step_number": idx + 1,
                "skill": skill,
                "domain": node_attrs.get("domain", "General"),
                "status": "Acquired" if is_already_acquired else "Next Goal",
                "difficulty_level": node_attrs.get("difficulty", 2),
                "study_weeks": step_weeks,
                "market_demand_index": node_attrs.get("demand", 85),
                "incremental_salary_boost_pct": step_boost,
                "running_salary_projection_usd": int(running_salary),
                "unlocks_downstream": unlocks,
                "milestone_description": f"Master {skill} ({node_attrs.get('domain', 'General')}) $\\to$ Unlocks {len(unlocks)} downstream technologies and boosts market compensation by +{step_boost}%."
            })

        total_months = round(cumulative_weeks / 4.33, 1)

        return {
            "target_role": target_role,
            "target_role_title": role_meta["title"],
            "algorithm_used": "Dijkstra Shortest Path Optimization" if algorithm.lower() != "astar" else "A* Heuristic Graph Search",
            "path_length": len([s for s in gps_steps if s["status"] != "Acquired"]),
            "total_nodes_in_path": len(path),
            "estimated_learning_time_weeks": cumulative_weeks,
            "estimated_learning_time_months": total_months,
            "expected_salary_growth_pct": f"+{round(cumulative_salary_boost, 1)}%",
            "final_projected_salary_usd": int(running_salary),
            "market_role_growth_5yr": role_meta["market_growth_pct"],
            "gps_trajectory": gps_steps,
            "trajectory_labels": [s["skill"] for s in gps_steps]
        }

# Global singleton
_gps_instance = None

def get_career_gps_engine() -> CareerGPSEngine:
    global _gps_instance
    if _gps_instance is None:
        _gps_instance = CareerGPSEngine()
    return _gps_instance
