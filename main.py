from datetime import date
from pathlib import Path
from challenge import (
    Challenge,
    create_challenge_today,
    load_challenges_csv,
    load_challenges_json,
    save_challenges_csv,
    save_challenges_json,
    print_challenges,
    status_completed,
    status_pendant,
)


def main():
    # day 4: load data - read and reconstruct the challenges
    json_path = Path("challenges.json")
    
    #try to load challenges that already exists
    if json_path.exists():
        print("file found, loading challenges...")
        challenges = load_challenges_json(json_path)
        print(f"loaded {len(challenges)} challenges from {json_path}")
        print_challenges(challenges)
        print("-completed challenges-")
        print_challenges(challenges, status_completed)
        print("-pending chalenges-")
        print_challenges(challenges, status_pendant)
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
    
    #save all the challenges
    save_challenges_json(json_path, challenges)
    save_challenges_csv("challenges.csv", challenges)
    print(f"saved {len(challenges)} challenges in database")
    
    # reload from file to verify reconstruction
    print(f"reconstructing challenges from json files: ")
    reloaded_json = load_challenges_json(json_path)
    print_challenges(reloaded_json)
    print_challenges(reloaded_json, status_pendant)
    print_challenges(reloaded_json, status_completed)
        
    print("reconstructing challenges from CSV files")
    reloaded_csv = load_challenges_csv("challenges.csv")
    print_challenges(reloaded_csv)
    print_challenges(reloaded_csv, status_pendant)
    print_challenges(reloaded_csv, status_completed)
        
    


if __name__ == "__main__":
    main()