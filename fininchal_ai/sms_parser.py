import re


def parse_sms(sms_text):
    raw = str(sms_text or "").strip()
    if not raw:
        return None

    amount = _extract_amount(raw)
    if amount is None:
        return None

    lower = raw.lower()
    if "credit" in lower or "credited" in lower:
        transaction_type = "credit"
    else:
        transaction_type = "debit"

    return {
        "amount": amount,
        "merchant": _extract_merchant(raw),
        "transaction_type": transaction_type,
        "bank": _extract_bank(raw),
        "raw_sms": raw,
    }


def parse_multiple_sms(text_block):
    results = []
    for line in str(text_block or "").splitlines():
        parsed = parse_sms(line)
        if parsed:
            results.append(parsed)
    return results


def _extract_amount(text):
    patterns = [
        r"(?:Rs\.?|INR|₹)\s*([0-9][0-9,]*(?:\.\d{1,2})?)",
        r"(?:debited|credited|spent|payment of|by)\s*(?:Rs\.?|INR|₹)?\s*([0-9][0-9,]*(?:\.\d{1,2})?)",
        r"UPI/([0-9][0-9,]*(?:\.\d{1,2})?)/",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                return None
    return None


def _extract_merchant(text):
    patterns = [
        r"\bat\s+([A-Za-z][A-Za-z0-9 &.-]+)",
        r"\bto\s+([A-Za-z][A-Za-z0-9 &.-]+)",
        r"\bfor\s+(?:UPI/)?([A-Za-z][A-Za-z0-9 &.-]+)",
        r"UPI/[0-9.,]+/([A-Za-z][A-Za-z0-9 &.-]+)",
        r"\bspent\s+(?:on|at)\s+([A-Za-z][A-Za-z0-9 &.-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            merchant = re.split(r"\s+(?:on|successful|from|trf|ref|txn)\b", match.group(1), flags=re.IGNORECASE)[0]
            return merchant.strip(" .-/") or "Unknown"
    return "Unknown"


def _extract_bank(text):
    lower = text.lower()
    if "hdfc" in lower:
        return "HDFC"
    if "icici" in lower:
        return "ICICI"
    if "sbi" in lower:
        return "SBI"
    if "kotak" in lower:
        return "Kotak"
    if "paytm" in lower:
        return "Paytm"
    return "Unknown"
