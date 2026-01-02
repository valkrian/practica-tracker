import unittest
from datetime import date
import json
from practica_tracker.challenge import Challenge, save_challenges_csv, load_challenges_csv, status_pendant
from pathlib import Path

class TestChallenge(unittest.TestCase):
    def test_json_roundtrip(self):
        c = Challenge(date=date(2026, 1, 2), description="Test roundtrip", status=status_pendant)
        data = c.to_dict()
        s = json.dumps(data)
        loaded = json.loads(s)
        c2 = Challenge.from_dict(loaded)
        self.assertEqual(c2.date, c.date)
        self.assertEqual(c2.description, c.description)
        self.assertEqual(c2.status, c.status)

    def test_from_dict_strips_and_defaults(self):
        raw = {"date": "2026-01-02 ", "description": "  hello world  ", "status": " pending "}
        c = Challenge.from_dict(raw)
        self.assertEqual(c.date, date(2026, 1, 2))
        self.assertEqual(c.description, "hello world")
        self.assertEqual(c.status, status_pendant)

        raw2 = {"date": "2026-01-03", "description": "desc", "status": ""}
        c2 = Challenge.from_dict(raw2)
        self.assertEqual(c2.status, status_pendant)

    def test_csv_roundtrip(self):
        p = Path("test_challenges.csv")
        try:
            c1 = Challenge(date=date(2026, 1, 1), description="A", status=status_pendant)
            c2 = Challenge(date=date(2026, 1, 2), description="B", status=status_pendant)
            save_challenges_csv(p, [c1, c2])
            loaded = load_challenges_csv(p)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].date, c1.date)
            self.assertEqual(loaded[0].description, c1.description)
        finally:
            if p.exists():
                p.unlink()

    def test_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            Challenge(date=date.today(), description="x", status="invalid")

if __name__ == '__main__':
    unittest.main()
