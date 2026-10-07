import json
import networkx as nx
from typing import List, Dict, Any, Set, Tuple, Optional
from pathlib import Path
from src.config.settings import KG_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

GRAPH_DATA_FILE = KG_DIR / 'skill_knowledge_graph.json'

class SkillKnowledgeGraph:
    """
    Skill Knowledge Graph engine backed by NetworkX.
    Models skill nodes, prerequisites, domains, difficulty levels, and career path trajectories.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_default_graph()

    def _build_default_graph(self):
        """Constructs an industry-standard ontology graph of tech and data skills."""
        # 1. Add Skill Nodes with Metadata
        nodes = [
            # Core Programming & Math
            {"id": "Python", "domain": "Core Programming", "level": "Foundational", "demand": 98, "difficulty": 1},
            {"id": "R", "domain": "Core Programming", "level": "Foundational", "demand": 75, "difficulty": 1},
            {"id": "SQL", "domain": "Data Management", "level": "Foundational", "demand": 95, "difficulty": 1},
            {"id": "Linear Algebra", "domain": "Math & Statistics", "level": "Foundational", "demand": 82, "difficulty": 2},
            {"id": "Calculus", "domain": "Math & Statistics", "level": "Foundational", "demand": 78, "difficulty": 2},
            {"id": "Probability & Statistics", "domain": "Math & Statistics", "level": "Foundational", "demand": 92, "difficulty": 2},
            
            # Data Wrangling & Analysis
            {"id": "NumPy", "domain": "Data Engineering & Prep", "level": "Intermediate", "demand": 90, "difficulty": 2},
            {"id": "Pandas", "domain": "Data Engineering & Prep", "level": "Intermediate", "demand": 94, "difficulty": 2},
            {"id": "Data Cleaning", "domain": "Data Engineering & Prep", "level": "Foundational", "demand": 88, "difficulty": 1},
            {"id": "EDA", "domain": "Data Analytics", "level": "Foundational", "demand": 89, "difficulty": 1},
            
            # Visualization & Storytelling
            {"id": "Matplotlib", "domain": "Data Visualization", "level": "Intermediate", "demand": 80, "difficulty": 2},
            {"id": "Seaborn", "domain": "Data Visualization", "level": "Intermediate", "demand": 82, "difficulty": 2},
            {"id": "Tableau", "domain": "Business Intelligence", "level": "Intermediate", "demand": 86, "difficulty": 2},
            {"id": "Power BI", "domain": "Business Intelligence", "level": "Intermediate", "demand": 89, "difficulty": 2},
            {"id": "Executive Storytelling", "domain": "Business Intelligence", "level": "Advanced", "demand": 85, "difficulty": 3},
            
            # Classical Machine Learning
            {"id": "Scikit-Learn", "domain": "Machine Learning", "level": "Intermediate", "demand": 92, "difficulty": 3},
            {"id": "Feature Engineering", "domain": "Machine Learning", "level": "Intermediate", "demand": 89, "difficulty": 3},
            {"id": "Model Evaluation", "domain": "Machine Learning", "level": "Intermediate", "demand": 88, "difficulty": 2},
            {"id": "XGBoost", "domain": "Machine Learning", "level": "Advanced", "demand": 91, "difficulty": 3},
            {"id": "LightGBM", "domain": "Machine Learning", "level": "Advanced", "demand": 87, "difficulty": 3},
            
            # Deep Learning & AI
            {"id": "Deep Learning", "domain": "Artificial Intelligence", "level": "Advanced", "demand": 93, "difficulty": 4},
            {"id": "PyTorch", "domain": "Artificial Intelligence", "level": "Advanced", "demand": 95, "difficulty": 4},
            {"id": "TensorFlow", "domain": "Artificial Intelligence", "level": "Advanced", "demand": 88, "difficulty": 4},
            {"id": "Computer Vision", "domain": "Artificial Intelligence", "level": "Specialized", "demand": 84, "difficulty": 4},
            {"id": "NLP", "domain": "Artificial Intelligence", "level": "Specialized", "demand": 94, "difficulty": 4},
            {"id": "Transformers", "domain": "Generative AI", "level": "Specialized", "demand": 97, "difficulty": 5},
            {"id": "LLMs", "domain": "Generative AI", "level": "Specialized", "demand": 99, "difficulty": 5},
            {"id": "RAG Architectures", "domain": "Generative AI", "level": "Specialized", "demand": 96, "difficulty": 4},
            
            # Big Data & Distributed Systems
            {"id": "Apache Spark", "domain": "Big Data Engineering", "level": "Advanced", "demand": 89, "difficulty": 4},
            {"id": "PySpark", "domain": "Big Data Engineering", "level": "Advanced", "demand": 88, "difficulty": 3},
            {"id": "Airflow", "domain": "Data Engineering & Prep", "level": "Advanced", "demand": 86, "difficulty": 3},
            {"id": "Kafka", "domain": "Big Data Engineering", "level": "Advanced", "demand": 84, "difficulty": 4},
            
            # MLOps & Production
            {"id": "Git", "domain": "Software Engineering", "level": "Foundational", "demand": 95, "difficulty": 1},
            {"id": "Docker", "domain": "Cloud & DevOps", "level": "Intermediate", "demand": 93, "difficulty": 3},
            {"id": "Kubernetes", "domain": "Cloud & DevOps", "level": "Advanced", "demand": 88, "difficulty": 4},
            {"id": "FastAPI", "domain": "Software Engineering", "level": "Intermediate", "demand": 89, "difficulty": 2},
            {"id": "CI/CD", "domain": "Cloud & DevOps", "level": "Intermediate", "demand": 87, "difficulty": 3},
            {"id": "MLflow", "domain": "MLOps", "level": "Advanced", "demand": 90, "difficulty": 3},
            {"id": "Model Monitoring", "domain": "MLOps", "level": "Advanced", "demand": 89, "difficulty": 3},
            {"id": "Cloud Computing (AWS/GCP)", "domain": "Cloud & DevOps", "level": "Intermediate", "demand": 94, "difficulty": 3}
        ]

        for node in nodes:
            self.graph.add_node(
                node["id"],
                domain=node["domain"],
                level=node["level"],
                demand=node["demand"],
                difficulty=node["difficulty"]
            )

        # 2. Directed Edges (Source -> Target represents "Source IS PREREQUISITE FOR Target")
        prerequisites = [
            ("Python", "NumPy"),
            ("Python", "Pandas"),
            ("Python", "FastAPI"),
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
            ("Matplotlib", "Seaborn"),
            ("SQL", "Data Cleaning"),
            ("SQL", "Tableau"),
            ("SQL", "Power BI"),
            ("Tableau", "Executive Storytelling"),
            ("Power BI", "Executive Storytelling"),
            ("Scikit-Learn", "XGBoost"),
            ("Scikit-Learn", "LightGBM"),
            ("Scikit-Learn", "Model Evaluation"),
            ("Scikit-Learn", "Deep Learning"),
            ("Deep Learning", "PyTorch"),
            ("Deep Learning", "TensorFlow"),
            ("Deep Learning", "NLP"),
            ("Deep Learning", "Computer Vision"),
            ("PyTorch", "Transformers"),
            ("TensorFlow", "Transformers"),
            ("Transformers", "LLMs"),
            ("Transformers", "RAG Architectures"),
            ("Python", "PySpark"),
            ("Apache Spark", "PySpark"),
            ("SQL", "Apache Spark"),
            ("Git", "CI/CD"),
            ("Docker", "Kubernetes"),
            ("Docker", "MLflow"),
            ("FastAPI", "Model Monitoring"),
            ("Scikit-Learn", "MLflow"),
            ("Cloud Computing (AWS/GCP)", "Kubernetes"),
            ("Cloud Computing (AWS/GCP)", "Airflow"),
            ("MLflow", "Model Monitoring")
        ]

        for u, v in prerequisites:
            self.graph.add_edge(u, v, relation="PREREQUISITE_FOR")

        logger.info(f"Knowledge Graph initialized with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")
        self.save_graph()

    def save_graph(self):
        """Serializes the graph to JSON format for backend and frontend consumption."""
        try:
            KG_DIR.mkdir(parents=True, exist_ok=True)
            data = self.to_dict()
            with open(GRAPH_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save graph data: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Converts graph into node-link data structure for frontend visualization."""
        nodes = []
        for n, d in self.graph.nodes(data=True):
            nodes.append({
                "id": n,
                "label": n,
                "domain": d.get("domain", "General"),
                "level": d.get("level", "Intermediate"),
                "demand": d.get("demand", 80),
                "difficulty": d.get("difficulty", 2),
                "in_degree": self.graph.in_degree(n),
                "out_degree": self.graph.out_degree(n)
            })

        edges = []
        for u, v, d in self.graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "relation": d.get("relation", "PREREQUISITE_FOR")
            })

        return {"nodes": nodes, "edges": edges}

    def detect_hidden_skill_gaps(self, candidate_skills: List[str], target_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Identifies hidden root prerequisites that the candidate is missing before they can learn target skills.
        Example: If target is TensorFlow and candidate lacks Python/NumPy, those are flagged as root blocker gaps.
        """
        cand_set = {s.strip().lower() for s in candidate_skills}
        target_set = [s.strip() for s in target_skills if s.strip()]

        hidden_gaps = []
        visited = set()

        for target in target_set:
            # Find matching node in graph (case insensitive)
            match_node = None
            for n in self.graph.nodes:
                if n.lower() == target.lower():
                    match_node = n
                    break
            
            if not match_node:
                continue

            # Ancestors are all direct and indirect prerequisites
            try:
                ancestors = nx.ancestors(self.graph, match_node)
                for anc in ancestors:
                    if anc.lower() not in cand_set and anc not in visited:
                        visited.add(anc)
                        node_data = self.graph.nodes[anc]
                        hidden_gaps.append({
                            "skill": anc,
                            "required_for": match_node,
                            "type": "Fundamental Prerequisite Blocker",
                            "domain": node_data.get("domain", "General"),
                            "difficulty": node_data.get("difficulty", 1),
                            "priority": "HIGH" if node_data.get("difficulty", 1) <= 2 else "MEDIUM"
                        })
            except Exception as e:
                logger.debug(f"Error checking ancestors for {match_node}: {e}")

        return sorted(hidden_gaps, key=lambda x: x["difficulty"])

    def get_skill_dependencies(self, skill: str) -> Dict[str, Any]:
        """Returns direct prerequisites, upstream ancestors, and downstream skills unlocked."""
        match_node = None
        for n in self.graph.nodes:
            if n.lower() == skill.strip().lower():
                match_node = n
                break

        if not match_node:
            return {"skill": skill, "exists": False, "prerequisites": [], "unlocks": [], "ancestors": []}

        direct_prereqs = list(self.graph.predecessors(match_node))
        direct_unlocks = list(self.graph.successors(match_node))
        all_ancestors = list(nx.ancestors(self.graph, match_node))
        all_descendants = list(nx.descendants(self.graph, match_node))

        return {
            "skill": match_node,
            "exists": True,
            "domain": self.graph.nodes[match_node].get("domain", "General"),
            "direct_prerequisites": direct_prereqs,
            "unlocks_skills": direct_unlocks,
            "full_upstream_chain": all_ancestors,
            "full_downstream_reach": all_descendants
        }

    def recommend_next_skills(self, candidate_skills: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Recommends the best next skills where the candidate has already satisfied the prerequisites.
        """
        cand_set = {s.strip().lower() for s in candidate_skills}
        candidates_unlocked = []

        for node in self.graph.nodes:
            if node.lower() in cand_set:
                continue

            prereqs = list(self.graph.predecessors(node))
            if not prereqs:
                # Foundational skill not yet acquired
                cand_score = 70.0
                readiness = 100.0
            else:
                satisfied = sum(1 for p in prereqs if p.lower() in cand_set)
                readiness = (satisfied / len(prereqs)) * 100.0
                cand_score = readiness * (self.graph.nodes[node].get("demand", 80) / 100.0)

            if readiness >= 50.0:  # Candidate has at least half prerequisites
                node_data = self.graph.nodes[node]
                candidates_unlocked.append({
                    "skill": node,
                    "domain": node_data.get("domain", "General"),
                    "level": node_data.get("level", "Intermediate"),
                    "demand_index": node_data.get("demand", 80),
                    "prerequisite_readiness_pct": round(readiness, 1),
                    "recommendation_score": round(cand_score, 1),
                    "missing_prerequisites": [p for p in prereqs if p.lower() not in cand_set]
                })

        candidates_unlocked.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return candidates_unlocked[:top_k]

    def discover_career_path(self, start_skill_or_role: str, target_skill_or_role: str) -> Dict[str, Any]:
        """
        Calculates the optimal shortest learning graph progression between two points.
        """
        def find_best_node(query: str):
            q = query.lower()
            for n in self.graph.nodes:
                if n.lower() == q:
                    return n
            for n in self.graph.nodes:
                if q in n.lower():
                    return n
            return None

        src = find_best_node(start_skill_or_role) or "Python"
        dst = find_best_node(target_skill_or_role) or "LLMs"

        try:
            if nx.has_path(self.graph, src, dst):
                path = nx.shortest_path(self.graph, src, dst)
            else:
                # Use ancestor intersection path
                path = [src] + list(nx.ancestors(self.graph, dst)) + [dst]
                path = list(dict.fromkeys(path))  # deduplicate preserving order
        except Exception:
            path = [src, dst]

        step_details = []
        for step in path:
            d = self.graph.nodes.get(step, {})
            step_details.append({
                "step_skill": step,
                "domain": d.get("domain", "General"),
                "difficulty": d.get("difficulty", 2),
                "demand": d.get("demand", 85)
            })

        return {
            "source": src,
            "target": dst,
            "total_steps": len(path),
            "trajectory_path": path,
            "step_details": step_details
        }

# Global singleton
_kg_instance = None

def get_knowledge_graph() -> SkillKnowledgeGraph:
    global _kg_instance
    if _kg_instance is None:
        _kg_instance = SkillKnowledgeGraph()
    return _kg_instance
