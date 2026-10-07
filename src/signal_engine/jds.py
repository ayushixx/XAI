from src.signal_engine.evidence import load_json
def get_jds_signal(signal):
    data = load_json("jds_evidence.json")
    return data.get(signal, {"status": "NO_VALIDATED_EVIDENCE"})
