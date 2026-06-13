KEYWORDS = {
    "Food": [
        "zomato", "swiggy", "blinkit", "dunzo", "restaurant", "cafe", "food",
        "hotel", "dining", "dominos", "pizza", "kfc", "mcdonalds", "burger",
        "biryani", "chai", "tea",
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "meesho", "nykaa", "ajio", "shopping",
        "mall", "store", "retail", "clothes", "fashion",
    ],
    "Transport": [
        "uber", "ola", "rapido", "metro", "bus", "auto", "transport", "petrol",
        "fuel", "parking", "toll", "irctc", "train", "flight", "indigo", "air",
    ],
    "Entertainment": [
        "netflix", "spotify", "youtube", "prime", "hotstar", "bookmyshow",
        "cinema", "movie", "game", "entertainment",
    ],
    "Health": [
        "apollo", "medplus", "pharmacy", "hospital", "doctor", "clinic",
        "medicine", "health", "gym", "fitness",
    ],
    "Banking": [
        "hdfc", "icici", "sbi", "kotak", "axis", "bank", "emi", "loan",
        "credit", "insurance", "lic",
    ],
    "Groceries": [
        "bigbasket", "jiomart", "dmart", "grofers", "zepto", "grocery",
        "vegetables", "milk", "fruits",
    ],
    "Utilities": [
        "electricity", "water", "gas", "internet", "wifi", "broadband",
        "airtel", "jio", "vodafone", "bsnl", "recharge", "mobile",
    ],
    "Savings": [
        "investment", "savings", "fd", "ppf", "elss", "sip", "mutual fund",
        "groww", "zerodha", "coin", "etmoney",
    ],
}


def categorize(text):
    text_lower = str(text or "").lower()
    for category, words in KEYWORDS.items():
        if any(keyword.lower() in text_lower for keyword in words):
            return category
    return "Other"
