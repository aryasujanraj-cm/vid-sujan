from collections import defaultdict
from datetime import datetime, timedelta


def analyze(expenses):
    total = 0.0
    category_data = defaultdict(float)
    monthly_data = defaultdict(float)

    for expense in expenses:
        try:
            amount = float(expense.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        category = expense.get("category") or "Other"
        date = expense.get("date") or ""
        month = date[:7] if len(date) >= 7 else "Unknown"

        total += amount
        category_data[category] += amount
        monthly_data[month] += amount

    return total, dict(category_data), dict(monthly_data)


def top_category(category_data):
    if not category_data:
        return "None"
    return max(category_data, key=category_data.get)


def spending_insights(total, category_data):
    if total <= 0:
        return ["💡 Add expenses to unlock spending insights."]

    insights = []
    for category, amount in category_data.items():
        percentage = (amount / total) * 100
        if percentage > 40:
            insights.append(f"⚠️ {category} is high at {percentage:.1f}% of spending.")
        elif percentage < 5:
            insights.append(f"✅ {category} is low at {percentage:.1f}% of spending.")
    return insights or ["✅ Your spending mix looks balanced so far."]


def monthly_trend(monthly_data):
    if len(monthly_data) < 2:
        return "➡️ Stable"
    months = sorted(monthly_data)
    first = monthly_data[months[0]]
    last = monthly_data[months[-1]]
    if last > first * 1.05:
        return "📈 Increasing"
    if last < first * 0.95:
        return "📉 Decreasing"
    return "➡️ Stable"


def budget_analysis(total, category_data):
    needs = ["food", "rent", "transport", "bills", "groceries", "utilities", "health"]
    wants = ["shopping", "entertainment", "travel", "dining"]
    savings = ["savings", "investment", "fd", "ppf", "elss", "sip", "mutual fund"]

    need_total = 0.0
    want_total = 0.0
    saving_total = 0.0

    for category, amount in category_data.items():
        category_lower = str(category).lower()
        if any(item.lower() == category_lower for item in needs):
            need_total += amount
        elif any(item.lower() == category_lower for item in wants):
            want_total += amount
        elif any(item.lower() == category_lower for item in savings):
            saving_total += amount

    if total <= 0:
        return {"needs": 0, "wants": 0, "savings": 0, "status": "No spending data yet"}

    return {
        "needs": (need_total / total) * 100,
        "wants": (want_total / total) * 100,
        "savings": (saving_total / total) * 100,
        "status": "Healthy" if need_total <= total * 0.5 and want_total <= total * 0.3 else "Needs attention",
    }


def detect_anomalies(expenses):
    now = datetime.now().date()
    category_totals = defaultdict(float)
    category_dates = defaultdict(list)
    recent_totals = defaultdict(float)

    for expense in expenses:
        category = expense.get("category") or "Other"
        try:
            amount = float(expense.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        try:
            date_value = datetime.strptime(str(expense.get("date", ""))[:10], "%Y-%m-%d").date()
        except ValueError:
            date_value = now

        category_totals[category] += amount
        category_dates[category].append(date_value)
        if date_value >= now - timedelta(days=7):
            recent_totals[category] += amount

    anomalies = []
    for category, total in category_totals.items():
        dates = category_dates[category]
        if not dates:
            continue
        span_days = max((max(dates) - min(dates)).days + 1, 7)
        usual_weekly = total / max(span_days / 7, 1)
        recent_weekly = recent_totals.get(category, 0.0)
        if usual_weekly <= 0:
            continue
        multiplier = recent_weekly / usual_weekly
        if multiplier > 2:
            alert_level = "danger" if multiplier >= 3 else "warning"
            anomalies.append({
                "category": category,
                "usual_weekly": usual_weekly,
                "recent_weekly": recent_weekly,
                "multiplier": multiplier,
                "alert_level": alert_level,
                "message": f"{category} spending is {multiplier:.1f}x your usual weekly level.",
            })
    return anomalies
