import csv
import json
from datetime import date
from pathlib import Path
from typing import Iterable, List

status_pendant = "pending"
status_completed = "completed"


class Challenge:
    def __init__(self, date: date, description: str, status: str = status_pendant):
        if status not in [status_pendant, status_completed]:
            raise ValueError(f"Invalid status: {status}")
        self.date = date
        self.description = description
        self.status = status

    def complete_challenge(self):
        self.status = status_completed

    def to_dict(self) -> dict:
        """Serialize the challenge to a JSON-friendly dict, transforms date into ISO format."""
        return {
            "date": self.date.isoformat(),
            "description": self.description,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Challenge":
        """Create a Challenge instance from a dict produced by to_dict, reconstructs challenge from dict."""
        return cls(
            date=date.fromisoformat(data["date"]),
            description=data["description"],
            status=data.get("status", status_pendant),
        )

    def __repr__(self) -> str:
        return (
            f"Challenge(date={self.date}, description='{self.description}', "
            f"status='{self.status}')"
        )


# helpers to save and load challenges ---

"""Those two functions are used type and read a list of challenges to and from a JSON file."""
def save_challenges_json(path: str | Path, challenges: Iterable[Challenge]) -> None:
    data = [c.to_dict() for c in challenges]
    Path(path).write_text(json.dumps(data, ensure_ascii=False , indent=2), encoding="utf-8")
    


def load_challenges_json(path: str | Path) -> List[Challenge]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Challenge.from_dict(item) for item in raw]



""" those two csv use dicwriter as a fixed header with date, description and status"""
def save_challenges_csv(path: str | Path, challenges: Iterable[Challenge]) -> None:
    fieldnames = ["date", "description", "status"]
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for challenge in challenges:
            writer.writerow(challenge.to_dict())


def load_challenges_csv(path: str | Path) -> List[Challenge]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [Challenge.from_dict(row) for row in reader]