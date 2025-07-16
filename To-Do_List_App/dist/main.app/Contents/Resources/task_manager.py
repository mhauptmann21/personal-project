import json
from models import Task

def load_tasks(filename="tasks.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Task.from_dict(task) for task in data]
    except FileNotFoundError:
        return[]
    
def save_tasks(tasks, filename="tasks.json"):
    with open(filename, "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def get_next_id(tasks):
    return max([task.id for task in tasks], default=0) + 1
