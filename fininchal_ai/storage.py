import json
import os
import shutil
from datetime import datetime

FILE = "expenses.json"


def get_user_path(username, filename):
    safe_username = "".join(ch for ch in str(username or "default") if ch.isalnum() or ch in ("_", "-")) or "default"
    folder = os.path.join("data", safe_username)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)


def user_data_dir(username="default"):
    safe_username = "".join(ch for ch in str(username or "default") if ch.isalnum() or ch in ("_", "-")) or "default"
    path = os.path.join("data", safe_username)
    os.makedirs(path, exist_ok=True)
    _ensure_user_guru(path)
    return path


def expense_path(username="default"):
    user_data_dir(username)
    return get_user_path(username, FILE)


def guru_path(username="default"):
    user_data_dir(username)
    return get_user_path(username, "guru.txt")


def load_expenses(username="default"):
    try:
        with open(expense_path(username), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def _write_expenses(expenses, username="default"):
    try:
        with open(expense_path(username), "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def save_expense(amount, category, merchant="Unknown", username="default"):
    expenses = load_expenses(username)
    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        amount_value = 0.0

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount_value,
        "category": category or "Other",
        "merchant": merchant or "Unknown",
    }
    expenses.append(expense)
    _write_expenses(expenses, username)
    return expense


def save_many_expenses(new_expenses, username="default"):
    expenses = load_expenses(username)
    today = datetime.now().strftime("%Y-%m-%d")
    clean_rows = []
    for item in new_expenses:
        try:
            amount = float(item.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        clean_rows.append({
            "date": item.get("date") or today,
            "amount": amount,
            "category": item.get("category") or "Other",
            "merchant": item.get("merchant") or "CSV Import",
        })
    expenses.extend(clean_rows)
    _write_expenses(expenses, username)
    return clean_rows


def _ensure_user_guru(path):
    destination = os.path.join(path, "guru.txt")
    if os.path.exists(destination):
        return
    try:
        if os.path.exists("guru.txt"):
            shutil.copyfile("guru.txt", destination)
        else:
            with open(destination, "w", encoding="utf-8") as f:
                f.write("Track every rupee — awareness is the first step to financial freedom\n")
    except OSError:
        pass
