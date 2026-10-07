from src.ai.router import route_intent
from src.ai.retriever import retrieve_context
from src.ai.agents import evidence_explainer, career_navigator, curriculum_planner, opportunity_radar

def process_query(query):
    intent = route_intent(query)
    context = retrieve_context(query)
    
    if not context:
        return "I do not have validated evidence for that in the supplied datasets."
        
    if intent == "curriculum_question":
        return curriculum_planner(query, context)
    elif intent == "career_question":
        return career_navigator(query, context)
    elif intent == "market_question":
        return opportunity_radar(query, context)
    else:
        # Default to evidence explainer for skill, evidence, success, or general questions
        return evidence_explainer(query, context)
