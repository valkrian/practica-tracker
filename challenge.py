from datetime import date

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
        
        
    def __repr__(self) -> str:
        return f"Challenge(date={self.date}, description='{self.description}', status='{self.status}')"