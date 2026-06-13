import streamlit as st
import google.generativeai as genai
import os
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


def show_book_advisor():
    st.subheader("📚 Book Advisor – Get AI Insights from Finance Books")

    key = st.secrets.get("GEMINI_API_KEY", "")
    if not key:
        st.error("GEMINI_API_KEY not found in secrets")
        return

    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    uploaded_file = st.file_uploader(
        "Upload a finance book PDF",
        type=["pdf"]
    )

    if not uploaded_file:
        st.info("Upload a PDF to get started")
        return

    cache_key = f"book_{uploaded_file.name}"
    if cache_key not in st.session_state:
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(uploaded_file)
        pages = [p.extract_text() for p in reader.pages if p.extract_text()]
        st.session_state[cache_key] = "\n".join(pages)

    book_text = st.session_state[cache_key]
    words = book_text.split()
    if len(words) > 12000:
        book_text = " ".join(words[:12000])

    st.success(f"Loaded {uploaded_file.name}")

    col1, col2, col3 = st.columns(3)
    quick = None
    if col1.button("📝 Summarise"):
        quick = "Give key financial lessons from this book"
    if col2.button("💡 Top 5 Tips"):
        quick = "List top 5 actionable money tips for Indian readers"
    if col3.button("🇮🇳 India Relevance"):
        quick = "Which concepts apply to Indian investors like SIP PPF tax saving"

    question = st.text_input("Ask a custom question about the book")
    if st.button("Ask Guru 🧙"):
        quick = question

    if quick:
        prompt = (
            f"You are Guru, an Indian finance advisor.\n\n"
            f"BOOK CONTENT:\n{book_text}\n\n"
            f"QUESTION:\n{quick}"
        )
        with st.spinner("Guru is thinking..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
