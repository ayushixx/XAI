from src.signal_engine.evidence import load_json
def get_sds_signal(signal):
    data = load_json("sds_evidence.json")
    return data.get(signal, {"status": "NO_VALIDATED_EVIDENCE"})
