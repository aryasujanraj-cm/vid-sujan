# book_advisor.py — uses Google Gemini API
# Functions: extract_book_text, get_book_advice, identify_book, show_book_advisor

import streamlit as st
import google.generativeai as genai
import os

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


def _get_model():
    key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not key:
        return None
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-2.0-flash")


def extract_book_text(uploaded_file) -> str:
    """Extract plain text from an uploaded PDF file."""
    if PyPDF2 is None:
        return ""
    try:
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(uploaded_file)
        pages = []
        for page in reader.pages[:10]:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n".join(pages)
    except Exception:
        return ""


def identify_book(book_text: str) -> str:
    """Try to identify the book title from extracted text."""
    if not book_text:
        return "Unknown Book"
    snippet = book_text[:500].lower()
    known_books = {
        "rich dad": "Rich Dad Poor Dad",
        "intelligent investor": "The Intelligent Investor",
        "psychology of money": "The Psychology of Money",
        "think and grow rich": "Think and Grow Rich",
        "atomic habits": "Atomic Habits",
        "zero to one": "Zero to One",
        "one up on wall street": "One Up on Wall Street",
        "millionaire next door": "The Millionaire Next Door",
        "your money or your life": "Your Money or Your Life",
        "i will teach you to be rich": "I Will Teach You to Be Rich",
    }
    for keyword, title in known_books.items():
        if keyword in snippet:
            return title
    return "Finance Book (uploaded)"


def get_book_advice(book_text: str, spending_summary: str) -> str:
    """Get Gemini AI advice based on book content and user spending."""
    model = _get_model()
    if model is None:
        return "⚠️ GEMINI_API_KEY not set. Add it in Streamlit Cloud → Settings → Secrets."

    words = book_text.split()
    if len(words) > 12000:
        book_text = " ".join(words[:12000])

    prompt = (
        "You are Guru, an expert Indian personal finance advisor. "
        "A user has uploaded a finance book. Based on the book content below, "
        "give 5 practical tips tailored to this user's spending habits. "
        "Make advice specific to Indian context (SIP, PPF, EMI, UPI, 80C) where relevant.\n\n"
        f"USER SPENDING: {spending_summary}\n\n"
        f"BOOK CONTENT:\n{book_text}\n\n"
        "Give exactly 5 numbered tips. Be concise and actionable."
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "⏳ Gemini quota reached. Please wait a few minutes and try again."
        return f"❌ Error: {e}"
