import re
import os
import numpy as np
from PIL import Image

_easyocr_reader = None

def _get_easyocr():
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            _easyocr_reader = easyocr.Reader(["en"], gpu=False)
        except Exception:
            _easyocr_reader = None
    return _easyocr_reader


def _get_groq_key():
    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY", "")


def _get_gemini():
    try:
        import google.generativeai as genai
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel("gemini-2.0-flash")
    except Exception:
        pass
    return None


# ── YOUR PERFECT LOGIC (unchanged) ───────────────────────────────────────────
def fix_symbols(text):
    text = str(text or "")
    replacements = {
        "Rs.": "₹", "Rs": "₹",
        "INR": "₹", "inr": "₹", "?": "₹",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def clean_text(text):
    text = str(text or "")
    text = re.sub(r"[^A-Za-z0-9₹$€.,:\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _to_float(value):
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def get_amount_candidates(text):
    text = str(text or "")
    candidates = []
    priority_patterns = [
        (r"(?:TOTAL|GRAND\s+TOTAL|AMOUNT|PAID)\s*[:\-]?\s*[₹$€]?\s*([0-9][0-9,]*(?:\.\d{1,2})?)", 100),
        (r"[₹$€]\s*([0-9][0-9,]*(?:\.\d{1,2})?)", 80),
    ]
    for pattern, score in priority_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            value = _to_float(match.group(1))
            if 10 <= value <= 100000:
                candidates.append({"amount": value, "score": score})
    for match in re.finditer(r"\b([0-9][0-9,]*(?:\.\d{1,2})?)\b", text):
        value = _to_float(match.group(1))
        if 10 <= value <= 100000:
            candidates.append({"amount": value, "score": 10})
    return candidates


def select_best_amount(candidates):
    if not candidates:
        return 0
    best = max(candidates, key=lambda item: (item["score"], item["amount"]))
    return best["amount"]


def extract_details(text):
    fixed_text = fix_symbols(text)
    currency = "₹"
    if "$" in fixed_text:
        currency = "$"
    elif "€" in fixed_text:
        currency = "€"
    elif "₹" in fixed_text:
        currency = "₹"
    cleaned = clean_text(fixed_text)
    amount = select_best_amount(get_amount_candidates(cleaned))
    merchant = "Unknown"
    skip_words = {
        "total", "grand", "amount", "paid", "payment", "debit", "credit",
        "transaction", "successful", "success", "date", "time",
    }
    for word in re.findall(r"\b[A-Za-z]{4,}\b", cleaned):
        if word.lower() not in skip_words:
            merchant = word
            break
    return merchant, amount, currency


# ── Groq cleans up messy OCR text ────────────────────────────────────────────
def _ask_groq(raw_ocr_text):
    groq_key = _get_groq_key()
    if not groq_key:
        return None, None

    try:
        import requests
        prompt = f"""You are a payment receipt parser.
Below is raw OCR text extracted from an Indian payment screenshot (UPI, PhonePe, GPay, Paytm, bank receipt).

RAW OCR TEXT:
{raw_ocr_text}

Extract ONLY:
1. The actual payment amount (NOT order ID, NOT transaction ID, just the rupee amount paid)
2. The merchant or shop name who received the payment

Reply in EXACTLY this format, nothing else:
AMOUNT: <number only, no symbols>
MERCHANT: <name>"""

        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0,
        }
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )
        data = resp.json()
        if "choices" not in data:
            return None, None

        reply = data["choices"][0]["message"]["content"]
        amount = None
        merchant = None
        for line in reply.splitlines():
            if line.startswith("AMOUNT:"):
                try:
                    amount = float(line.replace("AMOUNT:", "").strip().replace(",", ""))
                except Exception:
                    pass
            elif line.startswith("MERCHANT:"):
                merchant = line.replace("MERCHANT:", "").strip()
        return amount, merchant

    except Exception:
        return None, None


# ── OCR with easyocr ─────────────────────────────────────────────────────────
def _ocr_with_easyocr(image_file):
    reader = _get_easyocr()
    if reader is None:
        return ""
    image_file.seek(0)
    img = Image.open(image_file).convert("RGB")
    results = reader.readtext(np.array(img), detail=0)
    return " ".join(results)


# ── main functions ────────────────────────────────────────────────────────────
def extract_text_and_amount(image_file):
    # ── Option 1: Gemini Vision (best, if key available) ──────────────────
    model = _get_gemini()
    if model is not None:
        try:
            image_file.seek(0)
            img = Image.open(image_file)
            prompt = """This is a payment screenshot (UPI, PhonePe, GPay, Paytm, bank receipt).
Extract exactly:
1) Total amount paid (numbers only, NOT order ID or transaction ID)
2) Merchant or recipient name
3) All visible text

Reply in exactly this format:
AMOUNT: <number>
MERCHANT: <name>
TEXT: <all visible text>"""
            response = model.generate_content([prompt, img])
            raw = response.text
            fixed = fix_symbols(raw)
            text = clean_text(fixed)
            _merchant, amount, _currency = extract_details(text)
            return text, amount
        except Exception as e:
            if "429" not in str(e) and "quota" not in str(e).lower():
                return f"ERROR: {str(e)}", 0

    # ── Option 2: easyocr → Groq (no Gemini key needed) ──────────────────
    try:
        # Step 1: easyocr reads the image
        raw_text = _ocr_with_easyocr(image_file)
        if not raw_text:
            return "ERROR: Could not read image.", 0

        fixed_text = fix_symbols(raw_text)
        clean = clean_text(fixed_text)

        # Step 2: send raw text to Groq for smart parsing
        groq_amount, groq_merchant = _ask_groq(clean)

        # Step 3: build final text output
        amount = groq_amount if groq_amount and 1 <= groq_amount <= 999999 else select_best_amount(get_amount_candidates(clean))
        merchant = groq_merchant if groq_merchant and groq_merchant != "Unknown" else "Unknown"

        # Format like Gemini so extract_details works
        final_text = f"AMOUNT: {amount}\nMERCHANT: {merchant}\nTEXT: {clean}"
        return final_text, amount

    except Exception as e:
        return f"ERROR: {str(e)}", 0
