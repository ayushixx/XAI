from src.signal_engine.evidence import load_json
def get_market_signal(signal):
    data = load_json("market_evidence.json")
    return data.get(signal, {"status": "NO_VALIDATED_EVIDENCE"})
