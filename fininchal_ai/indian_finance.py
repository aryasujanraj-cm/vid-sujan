def sip_calculator(monthly_amount, annual_rate, years):
    monthly_amount = float(monthly_amount or 0)
    annual_rate = float(annual_rate or 0)
    years = float(years or 0)
    r = annual_rate / 12 / 100
    n = int(years * 12)
    if r == 0:
        return monthly_amount * n
    return monthly_amount * (((1 + r) ** n - 1) / r) * (1 + r)


def tax_saving_tips(annual_income, category_data):
    tips = []
    income = float(annual_income or 0)
    categories = [str(category).lower() for category in category_data]

    if income > 500000:
        tips.append("💸 Use Section 80C options like PPF, ELSS, LIC and EPF up to ₹1.5L.")
    if any(category.lower() == "health" for category in categories):
        tips.append("🏥 Explore Section 80D medical insurance deduction up to ₹25,000.")
    tips.append("🧾 Consider NPS for an additional ₹50,000 deduction under Section 80CCD(1B).")
    if any(category.lower() == "rent" for category in categories):
        tips.append("🏠 If eligible, claim HRA exemption for rent paid.")
    return tips


def compare_investments():
    principal = 100000
    years = 5
    rates = {
        "PPF": 7.1,
        "FD": 6.5,
        "MF-ELSS": 12.0,
        "SIP-index": 11.0,
    }
    return {
        name: {
            "rate": rate,
            "value": principal * ((1 + rate / 100) ** years),
        }
        for name, rate in rates.items()
    }


def check_50_30_20(total, category_data):
    needs = ["food", "rent", "transport", "bills", "groceries", "utilities", "health"]
    wants = ["shopping", "entertainment", "travel", "dining"]
    savings = ["savings", "investment", "fd", "ppf", "elss", "sip", "mutual fund"]

    buckets = {"needs": 0.0, "wants": 0.0, "savings": 0.0}
    total = float(total or 0)
    for category, amount in category_data.items():
        category_lower = str(category).lower()
        amount = float(amount or 0)
        if any(item.lower() == category_lower for item in needs):
            buckets["needs"] += amount
        elif any(item.lower() == category_lower for item in wants):
            buckets["wants"] += amount
        elif any(item.lower() == category_lower for item in savings):
            buckets["savings"] += amount

    if total <= 0:
        return {
            "needs_%": 0,
            "wants_%": 0,
            "savings_%": 0,
            "needs_healthy": False,
            "wants_healthy": False,
            "savings_healthy": False,
        }

    needs_pct = buckets["needs"] / total * 100
    wants_pct = buckets["wants"] / total * 100
    savings_pct = buckets["savings"] / total * 100
    return {
        "needs_%": needs_pct,
        "wants_%": wants_pct,
        "savings_%": savings_pct,
        "needs_healthy": needs_pct <= 50,
        "wants_healthy": wants_pct <= 30,
        "savings_healthy": savings_pct >= 20,
    }
