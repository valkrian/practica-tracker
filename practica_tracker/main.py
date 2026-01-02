"""CLI for practica-tracker.

Commands:

    practica-tracker list [--status pending|completed]
    practica-tracker add <description> [--complete]
    practica-tracker complete <ISO-date>

This module orchestrates domain helpers (challenge.*) and persistence helpers for CLI usage.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
import argparse
from practica_tracker.challenge import (
    create_challenge_today,
    load_challenges_csv,
    load_challenges_json,
    save_challenges_csv,
    save_challenges_json,
    print_challenges,
    status_completed,
    status_pendant,
    get_challenge_by_date,
)

DEFAULT_JSON = Path("challenges.json")
DEFAULT_CSV = Path("challenges.csv")


def cmd_list(args: argparse.Namespace) -> None:
    challenges = load_challenges_json(args.file)
    print_challenges(challenges, args.status)


def cmd_add(args: argparse.Namespace) -> None:
    challenges = load_challenges_json(args.file) if args.file.exists() else []
    today = date.today()
    existing = get_challenge_by_date(challenges, today)
    new_ch = create_challenge_today(args.description)
    if args.complete:
        new_ch.complete_challenge()
    if existing is None:
        challenges.append(new_ch)
        save_challenges_json(args.file, challenges)
        save_challenges_csv(DEFAULT_CSV, challenges)
        print("Added challenge:")
        print(new_ch)
    else:
        print("Challenge for today already exists:")
        print(existing)


def cmd_complete(args: argparse.Namespace) -> None:
    challenges = load_challenges_json(args.file)
    target_date = date.fromisoformat(args.date)
    ch = get_challenge_by_date(challenges, target_date)
    if ch is None:
        print(f"No challenge found for {target_date}")
        return
    ch.complete_challenge()
    save_challenges_json(args.file, challenges)
    save_challenges_csv(DEFAULT_CSV, challenges)
    print(f"Marked {target_date} as completed")


def interactive_flow() -> None:
    json_path = DEFAULT_JSON
    if json_path.exists():
        print("file found, loading challenges...")
        challenges = load_challenges_json(json_path)
        print(f"loaded {len(challenges)} challenges from {json_path}")
        print_challenges(challenges)
        print("-completed challenges-")
        print_challenges(challenges, status_completed)
        print("-pending challenges-")
        print_challenges(challenges, status_pendant)
        print()
    else:
        print("can't find the last file, starting a new challenge")
        challenges = []

    description = input("today's challenge: ")
    if not description.strip():
        description = "realizar un commit util en github"
    today_challenge = create_challenge_today(description)

    existing_today = get_challenge_by_date(challenges, date.today())
    if existing_today is None:
        print("adding new challenge: ")
        print(f"{today_challenge}")
        today_challenge.complete_challenge()
        challenges.append(today_challenge)
    else:
        print("challenge already exists, using the existing")

    save_challenges_json(json_path, challenges)
    save_challenges_csv(DEFAULT_CSV, challenges)
    print(f"saved {len(challenges)} challenges in database")

    # verify reconstruction
    print(f"reconstructing challenges from json files: ")
    reloaded_json = load_challenges_json(json_path)
    print_challenges(reloaded_json)
    print_challenges(reloaded_json, status_pendant)
    print_challenges(reloaded_json, status_completed)

    print("reconstructing challenges from CSV files")
    reloaded_csv = load_challenges_csv(DEFAULT_CSV)
    print_challenges(reloaded_csv)
    print_challenges(reloaded_csv, status_pendant)
    print_challenges(reloaded_csv, status_completed)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="practica-tracker")
    parser.add_argument("--file", type=Path, default=DEFAULT_JSON, help="JSON database file")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="List challenges")
    p_list.add_argument("--status", choices=[status_pendant, status_completed], help="Filter by status")

    p_add = sub.add_parser("add", help="Add today's challenge")
    p_add.add_argument("description", help="Description for today's challenge")
    p_add.add_argument("--complete", action="store_true", help="Mark as completed immediately")

    p_complete = sub.add_parser("complete", help="Mark a challenge completed by ISO date (YYYY-MM-DD)")
    p_complete.add_argument("date", help="Date of the challenge to mark completed (YYYY-MM-DD)")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.command == "list":
        cmd_list(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "complete":
        cmd_complete(args)
    else:
        interactive_flow()


if __name__ == "__main__":
    main()