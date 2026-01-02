"""Challenge domain model and (de)serialization helpers.


Responsibilities:
- Represent a daily challenge entry
- Convert to/from dict for JSON/CSV persistence
- Provide helpers to save/load lists of Challenge objects
"""

import csv
import json
from datetime import date
from pathlib import Path
from typing import Iterable, List

status_pendant = "pending"
status_completed = "completed"

#helpers
CSV_FIELDS = ["date", "description", "status"]
VALID_STATUSES = {status_pendant, status_completed} #helper for status


class Challenge:
    def __init__(self, date: date, description: str, status: str = status_pendant):
        # validate status strictly against allowed values
        if status not in VALID_STATUSES:
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
        """Create a Challenge instance from a dict produced by to_dict. This method is robust
        to whitespace and missing fields commonly found in CSV/JSON inputs."""
        # date: accept either a date object or an ISO date string (with whitespace)
        raw_date = data.get("date")
        if isinstance(raw_date, date):
            parsed_date = raw_date
        elif isinstance(raw_date, str):
            parsed_date = date.fromisoformat(raw_date.strip())
        else:
            raise ValueError("Missing or invalid date in challenge data")

        # description: normalize and strip
        raw_desc = data.get("description", "")
        description = raw_desc.strip()

        # status: normalize, default to pending if missing or empty
        raw_status = data.get("status")
        status = (raw_status or status_pendant).strip()
        if not status:
            status = status_pendant
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        return cls(
            date=parsed_date,
            description=description,
            status=status,
        )

    def __repr__(self) -> str:
        return (
            f"Challenge(date={self.date}, description='{self.description}', "
            f"status='{self.status}')"
        )


# helpers to save and load challenges ---

def save_challenges_json(path: str | Path, challenges: Iterable[Challenge]) -> None:
    data = [c.to_dict() for c in challenges]
    Path(path).write_text(json.dumps(data, ensure_ascii=False , indent=2), encoding="utf-8")


def load_challenges_json(path: str | Path) -> List[Challenge]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Challenge.from_dict(item) for item in raw]


def save_challenges_csv(path: str | Path, challenges: Iterable[Challenge]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for challenge in challenges:
            writer.writerow(challenge.to_dict())


def load_challenges_csv(path: str | Path) -> List[Challenge]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [Challenge.from_dict(row) for row in reader]


def get_challenge_by_date(challenges: List[Challenge], target_date: date) -> Challenge | None:
    """Find and returns a challenge by date. Returns None if not found."""
    for challenge in challenges:
        if challenge.date == target_date:
            return challenge
    return None


def create_challenge_today(description: str, status: str = status_pendant) -> Challenge:
    """create a new challenge with today's date"""
    return Challenge(
        date=date.today(),
        description=description,
        status=status,
    )


def mark_challenge_completed (challenge: Challenge) -> None:
    """Mark a challenge as completed."""
    challenge.complete_challenge()


def list_challenge_sorted (challenges: List[Challenge]) -> List[Challenge]:
    """returns a list of challenges sorted by date."""
    return sorted(challenges, key=lambda c: c.date)


def format_challenge(challenge: Challenge, index: int) -> str:
    """returns a legible line for a challenge"""
    return f"{index},{challenge.date} - {challenge.description} [{challenge.status}]"


def print_challenges(challenges: List[Challenge], status: str | None = None) -> None:
    """shows challenges ordered. optionally i can filter by status"""
    if status:
        if status not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        challenges = [c for c in challenges if c.status == status]
    challenges = sorted(challenges, key=lambda c: c.date)
    if not challenges:
        print("No challenges found.")
        return
    print(f"total challenges: {len(challenges)}")
    for i, challenge in enumerate(challenges, 1):
        print(format_challenge(challenge, i))


def filter_by_status (challenges: List[Challenge], status: str) -> List[Challenge]:
    """returns challenges filtered by status."""
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {VALID_STATUSES}")
    return [challenge for challenge in challenges if challenge.status == status]
