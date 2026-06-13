PRICE_LIST = {
    "iPhone 15": 79999,
    "Foreign Trip": 80000,
    "Bike": 100000,
    "MacBook": 120000,
    "Emergency Fund (6mo)": None,
    "Dream Wedding": 500000,
    "Car Down Payment": 200000,
}


def simulate_savings(current_spending, extra_monthly_saving, years=5):
    with_interest = _sip_value(extra_monthly_saving, 12, years)
    total_saved = float(extra_monthly_saving or 0) * int(years or 0) * 12
    emergency = float(current_spending or 0) * 6
    affordable = []
    for item, price in PRICE_LIST.items():
        value = emergency if price is None else price
        if with_interest >= value:
            affordable.append(item)
    return {
        "total_saved": total_saved,
        "with_interest": with_interest,
        "what_you_can_buy": affordable,
    }


def simulate_cut_spending(category, current_amount, cut_percent):
    monthly_saving = float(current_amount or 0) * float(cut_percent or 0) / 100
    yearly_saving = monthly_saving * 12
    return {
        "category": category,
        "monthly_saving": monthly_saving,
        "yearly_saving": yearly_saving,
        "five_year_value": _sip_value(monthly_saving, 12, 5),
    }


def _sip_value(monthly_amount, annual_rate, years):
    monthly_amount = float(monthly_amount or 0)
    r = float(annual_rate or 0) / 12 / 100
    n = int(float(years or 0) * 12)
    if r == 0:
        return monthly_amount * n
    return monthly_amount * (((1 + r) ** n - 1) / r) * (1 + r)
