"""Practica tracker package exports.


    Challenge helpers  ->  persistence (store)  ->  Flask app / CLI

This module re-exports the public API and exposes __version__.
"""

__version__ = "0.1.0"

from .challenge import (
    Challenge,
    create_challenge_today,
    get_challenge_by_date,
    load_challenges_csv,
    load_challenges_json,
    save_challenges_csv,
    save_challenges_json,
    print_challenges,
)
from .store import Entry, append_entry, read_entries, export_xlsx
from .main import main

__all__ = [
    "__version__",
    "Challenge",
    "create_challenge_today",
    "get_challenge_by_date",
    "load_challenges_csv",
    "load_challenges_json",
    "save_challenges_csv",
    "save_challenges_json",
    "print_challenges",
    "Entry",
    "append_entry",
    "read_entries",
    "export_xlsx",
    "main",
]
