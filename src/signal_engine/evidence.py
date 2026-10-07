import json
from pathlib import Path
from src.config.settings import BASE_DIR

ARTIFACTS_DIR = BASE_DIR / "artifacts"

def load_json(file_name):
    path = ARTIFACTS_DIR / file_name
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def get_evidence(evidence_id):
    for fn in ["market_evidence.json", "jds_evidence.json", "sds_evidence.json"]:
        data = load_json(fn)
        if evidence_id in data:
            return data[evidence_id]
    return {"status": "NO_VALIDATED_EVIDENCE"}

def get_signal(signal_name):
    return get_evidence(signal_name)
