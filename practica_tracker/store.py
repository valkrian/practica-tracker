"""Storage helpers for practica-tracker.

UML (excerpt):

    +--------+         +----------------+
    |  Entry |         |   CSV / XLSX   |
    | - id   |  ---->  | rows (persistence)
    | - date |
    | - desc |
    +--------+

Responsibilities:
- `Entry` dataclass represents a practice entry
- `append_entry` appends rows to CSV without overwriting
- `read_entries` reconstructs `Entry` instances
- `export_xlsx` provides optional Excel export (openpyxl)

Designed to be small and dependency-light.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, List
import uuid

CSV_FIELDS = ["id", "date", "time", "description", "tags", "duration_minutes"]


@dataclass
class Entry:
    id: str
    date: str  # ISO date YYYY-MM-DD
    time: str  # HH:MM
    description: str
    tags: str = ""
    duration_minutes: int = 0

    @classmethod
    def new(cls, description: str, date_iso: str | None = None, time_str: str | None = None, tags: str = "", duration_minutes: int = 0) -> "Entry":
        date_iso = date_iso or date.today().isoformat()
        time_str = time_str or datetime.now().strftime("%H:%M")
        return cls(id=str(uuid.uuid4()), date=date_iso, time=time_str, description=description.strip(), tags=tags.strip(), duration_minutes=int(duration_minutes))


def ensure_csv(path: Path) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def append_entry(path: Path, entry: Entry) -> None:
    ensure_csv(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(asdict(entry))


def read_entries(path: Path) -> List[Entry]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            rows.append(Entry(
                id=r.get("id", ""),
                date=r.get("date", ""),
                time=r.get("time", ""),
                description=r.get("description", ""),
                tags=r.get("tags", ""),
                duration_minutes=int(r.get("duration_minutes") or 0),
            ))
        return rows


def export_xlsx(csv_path: Path, xlsx_path: Path) -> None:
    try:
        from openpyxl import Workbook
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("openpyxl is required to export to XLSX") from exc

    entries = read_entries(csv_path)
    wb = Workbook()
    ws = wb.active
    ws.title = "Practica"
    ws.append(CSV_FIELDS)
    for e in entries:
        ws.append([e.id, e.date, e.time, e.description, e.tags, e.duration_minutes])
    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_path)
