from datetime import date
from pathlib import Path
from challenge import (
    Challenge,
    create_challenge_today,
    load_challenges_csv,
    load_challenges_json,
    save_challenges_csv,
    save_challenges_json,
)


def main():
    # day 4: load data - read and reconstruct the challenges
    json_path = Path("challenges.json")
    
    #try to load challenges that already exists
    if json_path.exists():
        print("file found, loading challenges...")
        challenges = load_challenges_json(json_path)
        print(f"loaded {len(challenges)} challenges from {json_path}")
        for i, challenge in enumerate(challenges, 1):
            print(f" {i}, {challenge}")
        print()
    else:
        print("can't find the last file, starting a new challenge")
        challenges = []
    
    #ask the user for a description
    description = input("today's challenge: ")
    if not description.strip(): #if blank, use description
            description = "realizar un commit util en github"
    today_challenge = create_challenge_today(description)
    

    #verifying if a challenge already exist
    today_str = date.today().isoformat()
    existing_today = [c for c in challenges if c.date.isoformat() == today_str]
    
    if not existing_today:
        print("adding new challenge: ")
        print(f"{today_challenge}")
        today_challenge.complete_challenge()
        challenges.append(today_challenge)
    else:
        print("challenge already exists, using the existing")
    
    #save all the challenges (including the new ones)
    save_challenges_json(json_path, challenges)
    save_challenges_csv("challenges.csv", challenges)
    print(f"saved {len(challenges)} challenges in database")
    
    # reload from file to verify reconstruction
    print(f"reconstructing challenges from json files: ")
    reloaded_json = load_challenges_json(json_path)
    for challenge in reloaded_json:
        print(f"{challenge}")
        
    print("reconstructing challenges from CSV files")
    reloaded_csv = load_challenges_csv("challenges.csv")
    for challenge in reloaded_csv:
        print(f"{challenge}")


if __name__ == "__main__":
    main()