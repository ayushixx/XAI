import unittest
from pathlib import Path

class TestUISmoke(unittest.TestCase):
    def test_app_exists(self):
        base = Path("e:/BUILD FOR BHARAT/8BIT_WORKFORCE_SIGNAL_ENGINE")
        self.assertTrue((base / "app/streamlit_app.py").exists())
        self.assertTrue((base / "app/views/capability.py").exists())
        self.assertTrue((base / "app/components/cards.py").exists())
