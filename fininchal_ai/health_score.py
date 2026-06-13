def calculate_health_score(total, category_data, goals, monthly_budget):
    total = float(total or 0)
    monthly_budget = float(monthly_budget or 0)
    goals = goals or []
    score = 100

    savings = _amount(category_data, ["savings", "investment", "fd", "ppf", "elss", "sip", "mutual fund"])
    food = _amount(category_data, ["food"])
    shopping = _amount(category_data, ["shopping"])
    wants = _amount(category_data, ["shopping", "entertainment", "travel", "dining"])

    savings_pct = savings / total * 100 if total else 0
    food_pct = food / total * 100 if total else 0
    shopping_pct = shopping / total * 100 if total else 0
    wants_pct = wants / total * 100 if total else 0

    if savings_pct < 10:
        score -= 20
    elif savings_pct < 20:
        score -= 10
    if food_pct > 40:
        score -= 15
    if shopping_pct > 30:
        score -= 10
    if wants_pct > 30:
        score -= 10
    if not goals:
        score -= 10
    if monthly_budget and total > monthly_budget:
        score -= 15
        if total > monthly_budget * 1.2:
            score -= 10

    if savings_pct > 20:
        score += 10
    if goals:
        score += 5
    if monthly_budget and total < monthly_budget * 0.6:
        score += 5

    score = max(0, min(100, int(score)))
    grade, label, color = get_grade(score)
    return {
        "score": score,
        "grade": grade,
        "label": label,
        "color": color,
        "breakdown": {
            "savings_score": max(0, min(30, int(savings_pct / 20 * 30))),
            "spending_score": max(0, 30 - int(max(food_pct - 40, 0) + max(wants_pct - 30, 0))),
            "budget_score": 20 if not monthly_budget or total <= monthly_budget else 5,
            "goals_score": 20 if goals else 5,
        },
        "tips": _tips(savings_pct, food_pct, shopping_pct, wants_pct, bool(goals), total, monthly_budget),
    }


def get_grade(score):
    if score >= 90:
        return "A+", "Excellent", "green"
    if score >= 80:
        return "A", "Good", "blue"
    if score >= 70:
        return "B+", "Above Average", "cyan"
    if score >= 60:
        return "B", "Average", "yellow"
    if score >= 50:
        return "C+", "Below Average", "orange"
    if score >= 40:
        return "C", "Poor", "orange"
    return "D/F", "Critical", "red"


def _amount(category_data, names):
    names = {name.lower() for name in names}
    return sum(float(amount or 0) for category, amount in (category_data or {}).items() if str(category).lower() in names)


def _tips(savings_pct, food_pct, shopping_pct, wants_pct, has_goals, total, monthly_budget):
    tips = []
    if savings_pct < 20:
        tips.append("Increase savings toward 20% by automating a SIP right after salary.")
    if food_pct > 40:
        tips.append("Food is high; set a weekly dining cap and plan two home meals.")
    if shopping_pct > 30 or wants_pct > 30:
        tips.append("Use a 24-hour pause before shopping or entertainment spends.")
    if monthly_budget and total > monthly_budget:
        tips.append("You are over budget; freeze optional spends until next month.")
    if not has_goals:
        tips.append("Create one concrete goal so monthly saving has a target.")
    tips.append("Review subscriptions and UPI auto-pay mandates this week.")
    return tips[:3]
