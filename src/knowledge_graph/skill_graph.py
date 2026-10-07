import json
import numpy as np
import networkx as nx
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Set

import src.utils.env_setup
from src.config.settings import DATA_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

KG_OUTPUT_DIR = DATA_DIR / "knowledge_graph"

class SkillKnowledgeGraph:
    """
    Production Directed Skill Knowledge Graph using NetworkX.
    Models prerequisite dependencies, domain co-occurrences, and topological centrality.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        KG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self._build_ontology_graph()

    def _build_ontology_graph(self) -> None:
        """Initializes standard 40+ node multi-domain skill topology."""
        nodes_data = [
            # Core Programming & Engineering
            ("Python", {"domain": "Core Programming", "level": 1, "demand_score": 98, "difficulty": 1.0, "time_weeks": 4}),
            ("R", {"domain": "Core Programming", "level": 1, "demand_score": 70, "difficulty": 1.5, "time_weeks": 4}),
            ("SQL", {"domain": "Database & Storage", "level": 1, "demand_score": 96, "difficulty": 1.0, "time_weeks": 3}),
            ("Git", {"domain": "Core Programming", "level": 1, "demand_score": 90, "difficulty": 1.0, "time_weeks": 2}),
            
            # Data Engineering & Foundation
            ("NumPy", {"domain": "Data Engineering", "level": 2, "demand_score": 90, "difficulty": 1.5, "time_weeks": 2}),
            ("Pandas", {"domain": "Data Engineering", "level": 2, "demand_score": 94, "difficulty": 1.5, "time_weeks": 3}),
            ("Data Cleaning", {"domain": "Data Engineering", "level": 2, "demand_score": 88, "difficulty": 1.5, "time_weeks": 3}),
            ("ETL Pipelines", {"domain": "Data Engineering", "level": 3, "demand_score": 91, "difficulty": 2.5, "time_weeks": 4}),
            ("PySpark", {"domain": "Big Data", "level": 3, "demand_score": 85, "difficulty": 3.0, "time_weeks": 5}),
            ("Data Warehousing", {"domain": "Big Data", "level": 3, "demand_score": 84, "difficulty": 2.5, "time_weeks": 4}),

            # Statistical Modeling & Classical ML
            ("Statistics", {"domain": "Mathematics & Stats", "level": 2, "demand_score": 89, "difficulty": 2.0, "time_weeks": 4}),
            ("Linear Algebra", {"domain": "Mathematics & Stats", "level": 2, "demand_score": 80, "difficulty": 2.5, "time_weeks": 4}),
            ("Machine Learning", {"domain": "Machine Learning", "level": 3, "demand_score": 95, "difficulty": 2.5, "time_weeks": 6}),
            ("Scikit-Learn", {"domain": "Machine Learning", "level": 3, "demand_score": 92, "difficulty": 2.0, "time_weeks": 4}),
            ("Feature Engineering", {"domain": "Machine Learning", "level": 3, "demand_score": 87, "difficulty": 2.0, "time_weeks": 3}),
            ("Model Evaluation", {"domain": "Machine Learning", "level": 3, "demand_score": 88, "difficulty": 2.0, "time_weeks": 3}),
            ("XGBoost", {"domain": "Machine Learning", "level": 3, "demand_score": 91, "difficulty": 2.5, "time_weeks": 3}),
            ("LightGBM", {"domain": "Machine Learning", "level": 3, "demand_score": 86, "difficulty": 2.5, "time_weeks": 3}),
            ("CatBoost", {"domain": "Machine Learning", "level": 3, "demand_score": 84, "difficulty": 2.5, "time_weeks": 3}),

            # Deep Learning & Generative AI
            ("Deep Learning", {"domain": "Artificial Intelligence", "level": 4, "demand_score": 93, "difficulty": 3.5, "time_weeks": 6}),
            ("PyTorch", {"domain": "Artificial Intelligence", "level": 4, "demand_score": 95, "difficulty": 3.5, "time_weeks": 6}),
            ("TensorFlow", {"domain": "Artificial Intelligence", "level": 4, "demand_score": 89, "difficulty": 3.5, "time_weeks": 6}),
            ("Computer Vision", {"domain": "Artificial Intelligence", "level": 4, "demand_score": 83, "difficulty": 3.5, "time_weeks": 5}),
            ("NLP", {"domain": "Artificial Intelligence", "level": 4, "demand_score": 92, "difficulty": 3.5, "time_weeks": 5}),
            ("Transformers", {"domain": "Generative AI", "level": 5, "demand_score": 97, "difficulty": 4.0, "time_weeks": 5}),
            ("LLMs", {"domain": "Generative AI", "level": 5, "demand_score": 99, "difficulty": 4.5, "time_weeks": 6}),
            ("RAG Architectures", {"domain": "Generative AI", "level": 5, "demand_score": 96, "difficulty": 4.0, "time_weeks": 4}),
            ("Prompt Engineering", {"domain": "Generative AI", "level": 4, "demand_score": 88, "difficulty": 2.0, "time_weeks": 2}),

            # Cloud, Deployment & MLOps
            ("Docker", {"domain": "DevOps / MLOps", "level": 3, "demand_score": 92, "difficulty": 2.5, "time_weeks": 3}),
            ("Kubernetes", {"domain": "DevOps / MLOps", "level": 4, "demand_score": 88, "difficulty": 3.5, "time_weeks": 5}),
            ("MLflow", {"domain": "DevOps / MLOps", "level": 3, "demand_score": 86, "difficulty": 2.5, "time_weeks": 3}),
            ("FastAPI", {"domain": "Backend & Serving", "level": 3, "demand_score": 90, "difficulty": 2.0, "time_weeks": 3}),
            ("MLOps", {"domain": "DevOps / MLOps", "level": 4, "demand_score": 94, "difficulty": 3.5, "time_weeks": 5}),
            ("AWS", {"domain": "Cloud Computing", "level": 3, "demand_score": 93, "difficulty": 3.0, "time_weeks": 4}),
            ("GCP", {"domain": "Cloud Computing", "level": 3, "demand_score": 89, "difficulty": 3.0, "time_weeks": 4}),

            # Business Intelligence & Storytelling
            ("Tableau", {"domain": "Business Intelligence", "level": 2, "demand_score": 86, "difficulty": 1.5, "time_weeks": 3}),
            ("Power BI", {"domain": "Business Intelligence", "level": 2, "demand_score": 89, "difficulty": 1.5, "time_weeks": 3}),
            ("Executive Storytelling", {"domain": "Business Intelligence", "level": 2, "demand_score": 85, "difficulty": 1.5, "time_weeks": 2})
        ]

        for node, attrs in nodes_data:
            self.graph.add_node(node, **attrs)

        # Directional Prerequisite & Advanced Edges (from prerequisite -> advanced)
        edges_data = [
            ("Python", "NumPy", {"type": "prerequisite", "weight": 1.2}),
            ("Python", "Pandas", {"type": "prerequisite", "weight": 1.3}),
            ("Python", "FastAPI", {"type": "advanced", "weight": 1.5}),
            ("Python", "PySpark", {"type": "advanced", "weight": 2.2}),
            ("NumPy", "Pandas", {"type": "related", "weight": 1.0}),
            ("NumPy", "Scikit-Learn", {"type": "prerequisite", "weight": 1.4}),
            ("Pandas", "Data Cleaning", {"type": "prerequisite", "weight": 1.1}),
            ("Pandas", "Feature Engineering", {"type": "prerequisite", "weight": 1.3}),
            ("SQL", "Data Warehousing", {"type": "prerequisite", "weight": 1.5}),
            ("SQL", "ETL Pipelines", {"type": "prerequisite", "weight": 1.6}),
            ("Statistics", "Machine Learning", {"type": "prerequisite", "weight": 1.8}),
            ("Linear Algebra", "Deep Learning", {"type": "prerequisite", "weight": 2.0}),
            ("Scikit-Learn", "Machine Learning", {"type": "related", "weight": 1.0}),
            ("Scikit-Learn", "Model Evaluation", {"type": "prerequisite", "weight": 1.2}),
            ("Scikit-Learn", "XGBoost", {"type": "advanced", "weight": 1.4}),
            ("Scikit-Learn", "LightGBM", {"type": "advanced", "weight": 1.4}),
            ("Scikit-Learn", "CatBoost", {"type": "advanced", "weight": 1.4}),
            ("Machine Learning", "Deep Learning", {"type": "prerequisite", "weight": 2.2}),
            ("Machine Learning", "Feature Engineering", {"type": "related", "weight": 1.1}),
            ("Deep Learning", "TensorFlow", {"type": "advanced", "weight": 1.8}),
            ("Deep Learning", "PyTorch", {"type": "advanced", "weight": 1.7}),
            ("Deep Learning", "Computer Vision", {"type": "advanced", "weight": 2.0}),
            ("Deep Learning", "NLP", {"type": "advanced", "weight": 2.0}),
            ("NLP", "Transformers", {"type": "prerequisite", "weight": 1.9}),
            ("PyTorch", "Transformers", {"type": "prerequisite", "weight": 1.6}),
            ("Transformers", "LLMs", {"type": "prerequisite", "weight": 1.8}),
            ("Transformers", "RAG Architectures", {"type": "prerequisite", "weight": 1.7}),
            ("LLMs", "RAG Architectures", {"type": "related", "weight": 1.2}),
            ("Prompt Engineering", "RAG Architectures", {"type": "related", "weight": 1.1}),
            ("Docker", "Kubernetes", {"type": "prerequisite", "weight": 2.0}),
            ("Docker", "MLOps", {"type": "prerequisite", "weight": 1.8}),
            ("FastAPI", "MLOps", {"type": "prerequisite", "weight": 1.6}),
            ("MLflow", "MLOps", {"type": "prerequisite", "weight": 1.4}),
            ("Machine Learning", "MLOps", {"type": "prerequisite", "weight": 2.4}),
            ("SQL", "Tableau", {"type": "prerequisite", "weight": 1.2}),
            ("SQL", "Power BI", {"type": "prerequisite", "weight": 1.2}),
            ("Tableau", "Executive Storytelling", {"type": "related", "weight": 1.1}),
            ("Power BI", "Executive Storytelling", {"type": "related", "weight": 1.1}),
            ("AWS", "MLOps", {"type": "related", "weight": 1.5}),
            ("GCP", "MLOps", {"type": "related", "weight": 1.5})
        ]

        for u, v, data in edges_data:
            self.graph.add_edge(u, v, **data)

        logger.info(f"Skill Knowledge Graph constructed with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")

    def compute_degree_centrality(self) -> Dict[str, float]:
        """Calculates in-degree and out-degree connectivity for each skill node."""
        return {k: round(v, 4) for k, v in nx.degree_centrality(self.graph).items()}

    def compute_betweenness_centrality(self) -> Dict[str, float]:
        """Calculates betweenness centrality (identifies bottleneck bridging skills)."""
        return {k: round(v, 4) for k, v in nx.betweenness_centrality(self.graph, weight="weight").items()}

    def compute_pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        """Calculates Google PageRank authority for each skill node in the dependency network."""
        return {k: round(v, 4) for k, v in nx.pagerank(self.graph, alpha=alpha, weight="weight").items()}

    def get_critical_skills(self, top_k: int = 8) -> List[Dict[str, Any]]:
        """
        Synthesizes PageRank, Betweenness Centrality, and Degree Centrality to identify
        the highest leverage, critical foundation skills in modern data/AI careers.
        """
        pr = self.compute_pagerank()
        bc = self.compute_betweenness_centrality()
        dc = self.compute_degree_centrality()

        critical = []
        for node in self.graph.nodes:
            attrs = self.graph.nodes[node]
            composite_score = (0.4 * pr.get(node, 0)) + (0.4 * bc.get(node, 0)) + (0.2 * dc.get(node, 0))
            critical.append({
                "skill": node,
                "domain": attrs.get("domain", "General"),
                "composite_centrality": round(composite_score * 100, 3),
                "pagerank": pr.get(node, 0),
                "betweenness": bc.get(node, 0),
                "degree": dc.get(node, 0),
                "market_demand_index": attrs.get("demand_score", 85)
            })

        critical.sort(key=lambda x: x["composite_centrality"], reverse=True)
        return critical[:top_k]

    def get_skill_dependencies(self, target_skill: str) -> Dict[str, Any]:
        """
        Returns all immediate and upstream ancestral prerequisites for a target skill.
        """
        if target_skill not in self.graph:
            return {"skill": target_skill, "direct_prerequisites": [], "all_ancestral_prerequisites": []}

        direct_prereqs = list(self.graph.predecessors(target_skill))
        all_ancestors = list(nx.ancestors(self.graph, target_skill))

        return {
            "skill": target_skill,
            "direct_prerequisites": direct_prereqs,
            "all_ancestral_prerequisites": all_ancestors,
            "total_upstream_count": len(all_ancestors)
        }

    def dijkstra_shortest_path(self, start_skill: str, target_skill: str) -> Optional[List[str]]:
        """
        Computes the shortest weighted prerequisite path using Dijkstra's algorithm.
        """
        if start_skill not in self.graph or target_skill not in self.graph:
            return None
        try:
            return nx.dijkstra_path(self.graph, start_skill, target_skill, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def astar_search_path(self, start_skill: str, target_skill: str) -> Optional[List[str]]:
        """
        Computes optimal graph trajectory using A* search with difficulty heuristics.
        """
        if start_skill not in self.graph or target_skill not in self.graph:
            return None

        def heuristic(u, v):
            lvl_u = self.graph.nodes[u].get("level", 1)
            lvl_v = self.graph.nodes[v].get("level", 1)
            return abs(lvl_v - lvl_u) * 0.5

        try:
            return nx.astar_path(self.graph, start_skill, target_skill, heuristic=heuristic, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_career_paths(self, start_skill: str = "Python") -> List[Dict[str, Any]]:
        """
        Generates standard high-growth career path trajectories from a foundation skill.
        """
        destinations = [
            ("LLMs", "Generative AI Architect"),
            ("MLOps", "MLOps & Infrastructure Engineer"),
            ("Computer Vision", "Computer Vision Specialist"),
            ("Executive Storytelling", "Lead Analytics Translator")
        ]

        paths = []
        for dest_skill, role_title in destinations:
            path = self.dijkstra_shortest_path(start_skill, dest_skill)
            if path:
                total_weeks = sum(self.graph.nodes[s].get("time_weeks", 3) for s in path)
                paths.append({
                    "target_role": role_title,
                    "target_skill": dest_skill,
                    "path_nodes": path,
                    "total_milestones": len(path),
                    "estimated_weeks": total_weeks,
                    "estimated_months": round(total_weeks / 4.33, 1)
                })
        return paths

# Global Singleton
_SKILL_GRAPH = None

def get_skill_graph() -> SkillKnowledgeGraph:
    global _SKILL_GRAPH
    if _SKILL_GRAPH is None:
        _SKILL_GRAPH = SkillKnowledgeGraph()
    return _SKILL_GRAPH
