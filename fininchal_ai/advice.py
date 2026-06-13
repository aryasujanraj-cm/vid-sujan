import os
import random


def load_guru(username="default"):
    paths_to_try = [
        os.path.join("data", username, "guru.txt"),
        "guru.txt",
        os.path.join("data", "default", "guru.txt"),
    ]
    for path in paths_to_try:
        try:
            with open(path, encoding="utf-8") as f:
                tips = [line.strip() for line in f.readlines() if line.strip()]
                if tips:
                    return tips
        except Exception:
            continue
    return [
        "Pay yourself first — save before you spend",
        "Start SIP early, even 500 rupees compounds big",
        "Track every rupee — awareness is first step",
        "Avoid EMIs for depreciating assets",
        "Build 6 months emergency fund first",
    ]


def give_advice(total, category_data, username="default"):
    advice = []
    total = float(total or 0)

    def category_amount(name):
        for category, amount in category_data.items():
            if str(category).lower() == name.lower():
                return float(amount or 0)
        return 0.0

    if total > 0:
        food = category_amount("Food")
        shopping = category_amount("Shopping")
        if food > total * 0.40:
            advice.append("⚠️ Food is above 40% of total spending. Try meal planning or weekly ordering limits.")
        if shopping > total * 0.30:
            advice.append("⚠️ Shopping is above 30% of spending. Use a 24-hour cooling period before purchases.")
        advice.append(f"💰 Target at least 20% savings this period: ₹{total * 0.20:,.2f}.")

    savings_present = any(str(category).lower() == "savings" for category in category_data)
    if not savings_present:
        advice.append("📈 No savings category found. Consider starting a monthly SIP, even with a small amount.")

    tips = load_guru(username)
    if tips:
        advice.append(f"🧠 Guru tip: {random.choice(tips)}")
    return advice or ["✅ Add spending data to receive personalized advice."]
