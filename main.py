from datetime import date
from challenge import Challenge

def main():
    
    today_challenge = Challenge(
        date=date.today(),
        description = "realizar un commit util en github",
    )
    
    print("recently created: ")
    print(today_challenge)


    today_challenge.complete_challenge()


    print("after completing: ")
    print(today_challenge)


if __name__ == "__main__":
    main()