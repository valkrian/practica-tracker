from datetime import date
from challenge import (
    Challenge,
    load_challenges_csv,
    load_challenges_json,
    save_challenges_csv,
    save_challenges_json,
)


def main():
    today_challenge = Challenge(
        date=date.today(),
        description="realizar un commit util en github",
    )

    print("recently created:")
    print(today_challenge)

    today_challenge.complete_challenge()

    print("after completing:")
    print(today_challenge)

    # Demo: persist and reload
    challenges = [today_challenge]
    save_challenges_json("challenges.json", challenges)
    save_challenges_csv("challenges.csv", challenges)

    print("loaded from JSON:", load_challenges_json("challenges.json"))
    print("loaded from CSV :", load_challenges_csv("challenges.csv"))


if __name__ == "__main__":
    main()