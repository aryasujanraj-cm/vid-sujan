def budget_analysis(total, category_data):
    needs = ["food", "rent", "transport", "bills", "groceries", "utilities", "health"]
    wants = ["shopping", "entertainment", "travel", "dining"]
    savings = ["savings", "investment", "fd", "ppf", "elss", "sip", "mutual fund"]

    need_total = 0.0
    want_total = 0.0
    saving_total = 0.0

    for category, amount in category_data.items():
        category_lower = str(category).lower()
        amount = float(amount or 0)
        if any(item.lower() == category_lower for item in needs):
            need_total += amount
        elif any(item.lower() == category_lower for item in wants):
            want_total += amount
        elif any(item.lower() == category_lower for item in savings):
            saving_total += amount

    if total <= 0:
        return ["💡 Add expenses to check your 50-30-20 budget health."]

    needs_limit = total * 0.50
    wants_limit = total * 0.30
    savings_target = total * 0.20
    savings_rate = (saving_total / total) * 100

    insights = []
    insights.append(
        f"{'✅' if need_total <= needs_limit else '⚠️'} Needs: ₹{need_total:,.2f} / ₹{needs_limit:,.2f}"
    )
    insights.append(
        f"{'✅' if want_total <= wants_limit else '⚠️'} Wants: ₹{want_total:,.2f} / ₹{wants_limit:,.2f}"
    )
    insights.append(
        f"{'✅' if saving_total >= savings_target else '⚠️'} Savings: ₹{saving_total:,.2f} / ₹{savings_target:,.2f}"
    )

    if savings_rate < 10:
        label = "poor"
    elif savings_rate < 20:
        label = "average"
    else:
        label = "good"
    insights.append(f"💰 Overall savings rate is {savings_rate:.1f}%: {label}.")
    return insights
