from datetime import datetime
from io import BytesIO

from fpdf import FPDF


def _safe_text(text):
    text = str(text).replace("₹", "Rs.").replace("—", "-")
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def generate_pdf_report(total, category_data, monthly_data, advice_list, budget_insights):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    content_width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _safe_text(f"Financial Report - {datetime.now().strftime('%B %Y')}"), ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, _safe_text(f"Total spending: ₹{float(total or 0):,.2f}"), ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Category Breakdown", ln=True)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(90, 8, "Category", border=1)
    pdf.cell(60, 8, "Amount", border=1, ln=True)
    pdf.set_font("Helvetica", "", 11)
    for category, amount in category_data.items():
        pdf.cell(90, 8, _safe_text(category), border=1)
        pdf.cell(60, 8, _safe_text(f"₹{float(amount or 0):,.2f}"), border=1, ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Monthly Trend", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for month, amount in monthly_data.items():
        pdf.cell(0, 7, _safe_text(f"{month}: ₹{float(amount or 0):,.2f}"), ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Top Advice", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for point in advice_list[:3]:
        pdf.multi_cell(content_width, 7, _safe_text(f"- {point}"))

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Budget Health Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for insight in budget_insights:
        pdf.multi_cell(content_width, 7, _safe_text(f"- {insight}"))

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(
        content_width,
        6,
        "Disclaimer: This report is educational only and is not certified financial advice.",
    )

    data = pdf.output(dest="S")
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, bytes):
        return data
    buffer = BytesIO()
    buffer.write(data.encode("latin-1"))
    return buffer.getvalue()
