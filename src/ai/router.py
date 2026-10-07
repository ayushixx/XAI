import re

def route_intent(query):
    query = query.lower()
    
    if any(k in query for k in ["why is", "explain", "evidence", "predictor"]):
        return "evidence_question"
    
    if any(k in query for k in ["learn first", "curriculum", "path"]):
        return "curriculum_question"
        
    if any(k in query for k in ["become", "career", "prioritize", "role"]):
        return "career_question"
        
    if any(k in query for k in ["market", "employers", "demanded", "salary", "visible"]):
        return "market_question"
        
    if any(k in query for k in ["success", "personality", "trait", "senior"]):
        return "success_question"
        
    if any(k in query for k in ["skill", "coding", "math", "stats"]):
        return "skill_question"
        
    return "general_project_question"
