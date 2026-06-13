# Financial Advisor AI

Financial Advisor AI is a Streamlit-based Indian personal finance app for expense tracking, OCR-based payment screenshot imports, budget monitoring, savings goals, Indian finance calculators, PDF reports, and an optional Gemini-powered financial guru chat.

> Disclaimer: This app is educational only and is not certified financial advice.

## Features

- Home dashboard with monthly spend, budget usage, top category, and recent transactions
- UPI/payment screenshot OCR using Gemini Vision and Pillow
- Manual expense entry and CSV bulk import
- Category analysis with Plotly bar, pie, and monthly trend charts
- 50-30-20 budget health checks and budget alerts
- Indian finance tools: SIP calculator, tax tips, PPF vs FD vs MF comparison
- Savings goals stored in `goals.json`
- Guru AI Chat with Gemini using spending context
- Splitwise-style bill splitter
- PDF report export using `fpdf2`

## Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
```

OCR uses the Google Gemini Vision API, so no system OCR package is required.
On Streamlit Community Cloud, leave `packages.txt` empty.

## Run

```bash
streamlit run app.py
```

The app creates `expenses.json` and `goals.json` automatically when data is saved.

## Gemini API Key

Guru AI Chat, Book Advisor, and screenshot OCR read `GEMINI_API_KEY` from Streamlit secrets or environment variables.

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

You can get a free Gemini API key from Google AI Studio.

## Folder Structure

```text
app.py
extract.py
categorize.py
analysis.py
advice.py
budget.py
storage.py
prediction.py
goals.py
indian_finance.py
export.py
requirements.txt
README.md
guru.txt
```

## Screenshots

Add screenshots here after running the app:

- Home dashboard
- Upload Screenshot OCR
- Analysis charts
- Indian Finance Advisor
- Export Report

## Notes

- `fix_symbols()` runs before `clean_text()` in OCR processing so currency symbols are preserved.
- Category matching uses lowercase comparisons on both sides.
- Prediction falls back to the current month when dates are missing.
- File reads return safe defaults when JSON files are missing or corrupt.
