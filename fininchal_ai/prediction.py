from collections import defaultdict
from datetime import datetime

from storage import load_expenses


def predict_monthly_spending(username="default"):
    expenses = load_expenses(username)
    if not expenses:
        return 0.0

    current_month = datetime.now().strftime("%Y-%m")
    monthly = defaultdict(float)
    all_amounts = []

    for expense in expenses:
        try:
            amount = float(expense.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        date = expense.get("date") or f"{current_month}-01"
        month = date[:7] if len(date) >= 7 else current_month
        monthly[month] += amount
        all_amounts.append(amount)

    if len(monthly) < 1:
        days_elapsed = max(datetime.now().day, 1)
        return (sum(all_amounts) / max(len(all_amounts), 1)) * 30 / days_elapsed

    if len(monthly) == 1:
        only_month = next(iter(monthly))
        if only_month == current_month:
            days_elapsed = max(datetime.now().day, 1)
            return monthly[only_month] / days_elapsed * 30
        return monthly[only_month]

    return sum(monthly.values()) / len(monthly)


def category_prediction():
    category_data = defaultdict(float)
    for expense in load_expenses():
        category = expense.get("category") or "Other"
        try:
            amount = float(expense.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        category_data[category] += amount
    return dict(category_data)
