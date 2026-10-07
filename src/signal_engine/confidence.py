import pandas as pd

def get_confidence(evidence_level, cv_auc, sample_size):
    cv_auc = cv_auc if pd.notna(cv_auc) else 0.0
    sample_size = sample_size if pd.notna(sample_size) else 0
    
    if evidence_level == "STRONG" and cv_auc >= 0.85 and sample_size >= 100:
        return "HIGH"
    elif evidence_level in ["STRONG", "EXPLORATORY"] and (cv_auc >= 0.70 or sample_size >= 50):
        return "MODERATE"
    else:
        return "LOW"
