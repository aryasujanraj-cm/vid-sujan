from datetime import datetime

from analysis import analyze


def generate_report_card(expenses, budget, goals):
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    previous_month = f"{now.year - 1}-12" if now.month == 1 else f"{now.year}-{now.month - 1:02d}"
    current_expenses = [item for item in expenses if str(item.get("date", "")).startswith(current_month)]
    previous_expenses = [item for item in expenses if str(item.get("date", "")).startswith(previous_month)]

    current_total, current_cats, _ = analyze(current_expenses)
    previous_total, _previous_cats, _ = analyze(previous_expenses)

    grades = {
        "Spending Control": grade_spending_control(current_total, previous_total),
        "Savings Rate": _grade_savings(current_total, current_cats),
        "Budget Adherence": _grade_budget(current_total, budget),
        "Goal Progress": _grade_goals(goals),
    }
    points = [_grade_points(value) for value in grades.values() if value != "N/A"]
    overall_points = sum(points) / len(points) if points else 0
    overall = _points_grade(overall_points)
    change = current_total - previous_total

    return {
        "grades": grades,
        "overall": overall,
        "points": overall_points,
        "insights": _insights(current_total, previous_total, current_cats, goals),
        "comparison": {
            "current": current_total,
            "previous": previous_total,
            "change": change,
            "direction": "up" if change > 0 else "down" if change < 0 else "flat",
        },
    }


def grade_spending_control(current, previous):
    if not previous:
        return "N/A"
    change = (current - previous) / previous * 100
    if change < -10:
        return "A+"
    if change < 0:
        return "A"
    if change < 5:
        return "B"
    if change < 15:
        return "C"
    return "D"


def _grade_savings(total, category_data):
    savings = sum(float(amount or 0) for cat, amount in category_data.items() if str(cat).lower() == "savings")
    pct = savings / total * 100 if total else 0
    if pct >= 30:
        return "A+"
    if pct >= 20:
        return "A"
    if pct >= 10:
        return "B"
    if pct >= 5:
        return "C"
    return "D"


def _grade_budget(total, budget):
    if not budget:
        return "N/A"
    used = total / budget * 100
    if used <= 60:
        return "A+"
    if used <= 80:
        return "A"
    if used <= 100:
        return "B"
    if used <= 120:
        return "C"
    return "D"


def _grade_goals(goals):
    if not goals:
        return "D"
    on_track = sum(1 for goal in goals if float(goal.get("monthly_saving", 0) or 0) > 0)
    pct = on_track / len(goals) * 100
    if pct >= 90:
        return "A+"
    if pct >= 75:
        return "A"
    if pct >= 50:
        return "B"
    return "C"


def _grade_points(grade):
    return {"A+": 95, "A": 85, "B": 70, "C": 55, "D": 35, "F": 20}.get(grade, 0)


def _points_grade(points):
    if points >= 90:
        return "A+"
    if points >= 80:
        return "A"
    if points >= 65:
        return "B"
    if points >= 50:
        return "C"
    return "D"


def _insights(current, previous, categories, goals):
    insights = []
    if previous and current < previous:
        insights.append("Spending improved versus last month.")
    elif previous:
        insights.append("Spending increased versus last month; review top categories.")
    else:
        insights.append("No previous month data yet, so this is your baseline.")
    if categories:
        top = max(categories, key=categories.get)
        insights.append(f"Top current-month category is {top}.")
    if goals:
        insights.append("You have active goals; keep funding them monthly.")
    else:
        insights.append("Add a goal to improve your report card.")
    return insights[:3]
