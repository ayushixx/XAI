import unittest
import json
from pathlib import Path
from src.config.settings import BASE_DIR

class TestEvidenceStore(unittest.TestCase):
    def test_sds_evidence(self):
        sds_path = BASE_DIR / "artifacts" / "sds_evidence.json"
        with open(sds_path, "r") as f:
            data = json.load(f)
        self.assertIn("conscientiousness", data)
        self.assertEqual(data["conscientiousness"]["evidence_level"], "STRONG")
        
    def test_source_dataset_exists(self):
        map_path = BASE_DIR / "artifacts" / "signal_map.json"
        with open(map_path, "r") as f:
            data = json.load(f)
        for sig_id, ev in data.items():
            self.assertIn(ev["domain"], ["MARKET", "JDS", "SDS"])
            self.assertIsNotNone(ev["sample_size"])
