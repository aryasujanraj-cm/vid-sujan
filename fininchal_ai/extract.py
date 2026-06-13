import re
import base64
import os
import google.generativeai as genai
from PIL import Image
import io


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
        raise ValueError("No GEMINI_API_KEY found")
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


def extract_text_and_amount(image_file):
    try:
        image_file.seek(0)
        model = get_gemini_client()
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
        merchant = "Unknown"

        for line in raw.splitlines():
            if line.startswith("AMOUNT:"):
                try:
                    amount = float(
                        line.replace("AMOUNT:", "")
                        .strip().replace(",", "")
                    )
                except Exception:
                    pass
            elif line.startswith("MERCHANT:"):
                merchant = line.replace(
                    "MERCHANT:", "").strip()

        fixed = fix_symbols(raw)
        text = clean_text(fixed)
        return text, amount

    except Exception as e:
        print("Vision Error:", e)
        return f"ERROR: {str(e)}", 0


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
            merchant = line.replace(
                "MERCHANT:", "").strip()
    return merchant, amount, currency
