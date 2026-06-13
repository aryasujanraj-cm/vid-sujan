import json
import math
import os
import uuid
from datetime import datetime

GOALS_FILE = "goals.json"


def get_user_path(username, filename):
    safe_username = "".join(ch for ch in str(username or "default") if ch.isalnum() or ch in ("_", "-")) or "default"
    folder = os.path.join("data", safe_username)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)


def _goal_path(username="default"):
    return get_user_path(username, GOALS_FILE)


def load_goals(username="default"):
    try:
        with open(_goal_path(username), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def _write_goals(goals, username="default"):
    try:
        with open(_goal_path(username), "w", encoding="utf-8") as f:
            json.dump(goals, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def save_goal(name, target, monthly_saving, username="default"):
    goals = load_goals(username)
    goal = {
        "id": str(uuid.uuid4()),
        "name": name,
        "target": float(target or 0),
        "monthly_saving": float(monthly_saving or 0),
        "created_date": datetime.now().strftime("%Y-%m-%d"),
    }
    goals.append(goal)
    _write_goals(goals, username)
    return goal


def delete_goal(goal_id, username="default"):
    goals = [goal for goal in load_goals(username) if goal.get("id") != goal_id]
    _write_goals(goals, username)
    return goals


def months_to_goal(target, monthly_saving):
    target = float(target or 0)
    monthly_saving = float(monthly_saving or 0)
    if monthly_saving <= 0:
        return 0
    return int(math.ceil(target / monthly_saving))
