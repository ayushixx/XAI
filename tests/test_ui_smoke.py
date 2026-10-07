import unittest
from pathlib import Path

class TestUISmoke(unittest.TestCase):
    def test_app_exists(self):
        base = Path(__file__).resolve().parent.parent
        self.assertTrue((base / "src/api/app.py").exists())
        self.assertTrue((base / "src/dashboard/index.html").exists())
        self.assertTrue((base / "app/streamlit_app.py").exists())
        self.assertTrue((base / "app/views/capability.py").exists())
        self.assertTrue((base / "app/components/cards.py").exists())
