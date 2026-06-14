import re
import os
import google.generativeai as genai
from PIL import Image

# ── easyocr loaded lazily to avoid slow startup ──────────────────────────────
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


def get_gemini_client():
    api_key = ""
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def fix_symbols(text):
    text = str(text or "")
    replacements = {
        "Rs.": "₹", "Rs": "₹",
        "INR": "₹", "inr": "₹", "?": "₹"
    }
    for s, t in replacements.items():
        text = text.replace(s, t)
    return text


def clean_text(text):
    text = str(text or "")
    text = re.sub(r"[^A-Za-z0-9₹$€.,:\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_with_easyocr(image_file):
    """Fallback: extract raw text using easyocr, then guess amount + merchant."""
    reader = _get_easyocr()
    if reader is None:
        return "ERROR: No OCR available. Add GEMINI_API_KEY to secrets.", 0.0

    image_file.seek(0)
    img = Image.open(image_file).convert("RGB")

    import numpy as np
    results = reader.readtext(np.array(img), detail=0)
    raw = " ".join(results)

    # Guess amount — find largest number in text
    amounts = re.findall(r"[\d,]+\.?\d*", raw)
    amount = 0.0
    for a in amounts:
        try:
            val = float(a.replace(",", ""))
            if val > amount:
                amount = val
        except Exception:
            pass

    # Guess merchant — first capitalized word group
    merchant = "Unknown"
    match = re.search(r"[A-Z][a-zA-Z]+([\s][A-Z][a-zA-Z]+)*", raw)
    if match:
        merchant = match.group(0)

    text = fix_symbols(raw)
    text = clean_text(text)

    # Format like Gemini so extract_details works
    formatted = f"AMOUNT: {amount}\nMERCHANT: {merchant}\nTEXT: {text}"
    return formatted, amount


def extract_text_and_amount(image_file):
    # ── Try Gemini first ──────────────────────────────────────────────────
    model = get_gemini_client()
    if model is not None:
        try:
            image_file.seek(0)
            img = Image.open(image_file)
            prompt = """This is a payment screenshot
            (UPI, PhonePe, GPay, Paytm, bank receipt).
            Extract exactly:
            1) Total amount paid (numbers only)
            2) Merchant or recipient name
            3) All visible text

            Reply in exactly this format:
            AMOUNT: <number>
            MERCHANT: <name>
            TEXT: <all visible text>"""
            response = model.generate_content([prompt, img])
            raw = response.text
            amount = 0.0
            for line in raw.splitlines():
                if line.startswith("AMOUNT:"):
                    try:
                        amount = float(
                            line.replace("AMOUNT:", "")
                            .strip().replace(",", "")
                        )
                    except Exception:
                        pass
            fixed = fix_symbols(raw)
            text = clean_text(fixed)
            return text, amount
        except Exception as e:
            err = str(e)
            # If quota hit → fall through to easyocr
            if "429" not in err and "quota" not in err.lower():
                return f"ERROR: {err}", 0.0
            # else fall through below

    # ── Fallback: easyocr ────────────────────────────────────────────────
    try:
        image_file.seek(0)
        return _extract_with_easyocr(image_file)
    except Exception as e:
        return f"ERROR: {str(e)}", 0.0


def extract_details(text):
    merchant = "Unknown"
    amount = 0.0
    currency = "₹"
    for line in str(text).splitlines():
        if line.startswith("AMOUNT:"):
            try:
                amount = float(
                    line.replace("AMOUNT:", "")
                    .strip().replace(",", "")
                )
            except Exception:
                pass
        elif line.startswith("MERCHANT:"):
            merchant = line.replace("MERCHANT:", "").strip()
    return merchant, amount, currency
