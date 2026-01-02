import unittest
from datetime import date
from pathlib import Path
import tempfile
from practica_tracker.main import main as cli_main
from practica_tracker.challenge import load_challenges_json, status_pendant, status_completed

class TestCLI(unittest.TestCase):
    def test_add_and_list(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "db.json"
            cli_main(["--file", str(db), "add", "CLI desc"])
            challenges = load_challenges_json(db)
            self.assertTrue(any(c.description == "CLI desc" for c in challenges))
            # list should not raise
            cli_main(["--file", str(db), "list"]) 

    def test_complete_command(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "db2.json"
            today = date.today().isoformat()
            cli_main(["--file", str(db), "add", "To complete"])
            cli_main(["--file", str(db), "complete", today])
            challenges = load_challenges_json(db)
            ch = next((c for c in challenges if c.date.isoformat() == today), None)
            self.assertIsNotNone(ch)
            self.assertEqual(ch.status, status_completed)

if __name__ == '__main__':
    unittest.main()
