def get_spending_personality(total, category_data, savings_rate):
    total = float(total or 0)

    def pct(name):
        amount = 0.0
        for category, value in (category_data or {}).items():
            if str(category).lower() == name.lower():
                amount += float(value or 0)
        return amount / total * 100 if total else 0

    food = pct("Food")
    shopping = pct("Shopping")
    savings = savings_rate
    transport = pct("Transport")
    entertainment = pct("Entertainment")
    max_category = max((float(v or 0) for v in (category_data or {}).values()), default=0)
    max_pct = max_category / total * 100 if total else 0

    if food > 35 and shopping < 15:
        return _profile("🍕", "The Foodie", "You live to eat! Food brings you joy but watch the budget", "Great at enjoying everyday life", "Dining can quietly drain savings", "Set a weekly food wallet.", "Spends like Ranveer Singh")
    if shopping > 35:
        return _profile("🛒", "The Shopaholic", "Retail therapy is real for you. Try a 24hr rule before buying", "You know what you like", "Impulse buys may pile up", "Use wishlists, then wait a day.", "Spends like Karan Johar")
    if savings > 30:
        return _profile("🐜", "The Super Saver", "You are amazing at saving! Make sure to enjoy life too", "Strong discipline", "May delay joy too much", "Budget guilt-free fun money.", "Spends like Ratan Tata")
    if transport > 25:
        return _profile("🚗", "The Road Warrior", "Always on the move! Consider carpooling or monthly passes", "High mobility", "Travel costs add up", "Try passes, pooling, or route planning.", "Spends like Virat Kohli")
    if entertainment > 20:
        return _profile("🎬", "The Experience Collector", "Life is for living! Balance experiences with future planning", "You invest in memories", "Subscriptions and outings can creep", "Cancel one unused subscription.", "Spends like Shah Rukh Khan")
    if savings < 5 and shopping > 20:
        return _profile("🦋", "The Impulse Buyer", "Living in the moment! Small changes now = big freedom later", "Spontaneous and energetic", "Savings can get ignored", "Automate savings before shopping.", "Spends like a Bollywood launch party")
    if total > 0 and max_pct <= 30:
        return _profile("🦉", "The Wise Spender", "Excellent balance! You have strong financial instincts", "Balanced habits", "Can still optimize goals", "Raise savings by 1% this month.", "Spends like Nandan Nilekani")
    return _profile("💫", "The Explorer", "Your unique spending style is still revealing itself", "Flexible and curious", "Patterns are not clear yet", "Track consistently for 30 days.", "Spends like a startup founder")


def _profile(emoji, title, description, strength, weakness, tip, celebrity_match):
    return {
        "emoji": emoji,
        "title": title,
        "description": description,
        "strength": strength,
        "weakness": weakness,
        "tip": tip,
        "celebrity_match": celebrity_match,
    }
