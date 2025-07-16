from datetime import datetime

class Task:
    def __init__(self, id, title, done=False, priority="mdedium", due_date=None):
        self.id = id
        self.title = title
        self.done = done
        self.priority = priority # low, medium, high
        self.due_date = due_date # string: 'YYYY-MM-DD'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }
    
    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            title=data["title"],
            done=data["done"],
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date")
        )
    
    def __str__(self):
        return f"{self.title} ({'✓' if self.done else '✗'})"