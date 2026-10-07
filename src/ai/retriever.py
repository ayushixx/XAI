import json
from src.config.settings import BASE_DIR

def get_signal_map():
    path = BASE_DIR / "artifacts" / "signal_map.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def retrieve_context(query):
    query = query.lower()
    signal_map = get_signal_map()
    
    matched_signals = []
    
    import re
    for sig_id, ev in signal_map.items():
        clean_sig = sig_id.replace("_", " ").lower()
        if re.search(r'\b' + re.escape(clean_sig) + r'\b', query):
            matched_signals.append(ev)
            
    # Handle aliases
    if "math" in query or "stat" in query:
        if "maths-stats_skills" in signal_map:
            matched_signals.append(signal_map["maths-stats_skills"])
            
    if "coding" in query:
        if "coding_skills" in signal_map:
            matched_signals.append(signal_map["coding_skills"])
            
    if "conscientiousness" in query:
        if "conscientiousness" in signal_map:
            matched_signals.append(signal_map["conscientiousness"])
            
    # Deduplicate
    unique_signals = {s["id"]: s for s in matched_signals}
    return list(unique_signals.values())
