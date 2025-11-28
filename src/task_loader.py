import json

def load_tasks(path="tasks/sample_tasks.json"):
    with open(path, "r") as f:
        return json.load(f)
