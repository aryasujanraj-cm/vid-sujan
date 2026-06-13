import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from advice import give_advice
from analysis import analyze, detect_anomalies, monthly_trend, spending_insights, top_category
from book_advisor import show_book_advisor
from budget import budget_analysis as rule_budget_analysis
from categorize import KEYWORDS, categorize
from export import generate_pdf_report
from extract import extract_details, extract_text_and_amount
from goals import delete_goal, load_goals, months_to_goal, save_goal
from health_score import calculate_health_score
from indian_finance import check_50_30_20, compare_investments, sip_calculator, tax_saving_tips
from personality import get_spending_personality
from prediction import predict_monthly_spending
from report_card import generate_report_card
from simulator import simulate_cut_spending, simulate_savings
from sms_parser import parse_multiple_sms
from storage import guru_path, load_expenses, save_expense, save_many_expenses, user_data_dir
from users import verify_login


st.set_page_config(page_title="💰 Financial Advisor AI", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{font-family:'Inter',sans-serif;box-sizing:border-box}
.stApp{background-color:#080c14;color:#e2e8f0}
.main .block-container{padding:2rem 3rem;max-width:1200px}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeInLeft{from{opacity:0;transform:translateX(-30px)}to{opacity:1;transform:translateX(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes gradientShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes glowPulse{0%,100%{text-shadow:0 0 10px rgba(34,211,238,0.5)}50%{text-shadow:0 0 30px rgba(34,211,238,1),0 0 60px rgba(34,211,238,0.5)}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(34,211,238,0.4)}70%{box-shadow:0 0 0 15px rgba(34,211,238,0)}100%{box-shadow:0 0 0 0 rgba(34,211,238,0)}}
@keyframes slideInRight{from{opacity:0;transform:translateX(50px)}to{opacity:1;transform:translateX(0)}}
@keyframes borderFlow{0%{border-color:#22d3ee}33%{border-color:#a78bfa}66%{border-color:#22c55e}100%{border-color:#22d3ee}}
@keyframes countUp{from{opacity:0;transform:scale(0.5)}to{opacity:1;transform:scale(1)}}
.hero-banner{background:linear-gradient(135deg,#0f172a,#1a1040,#0f2a1a);background-size:400% 400%;animation:gradientShift 8s ease infinite,fadeInUp 0.8s ease;border-radius:24px;padding:48px 40px;margin-bottom:32px;border:1px solid rgba(34,211,238,0.2);position:relative;overflow:hidden}
.hero-banner::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(34,211,238,0.05) 0%,transparent 60%)}
.hero-title{font-size:2.8rem;font-weight:800;background:linear-gradient(135deg,#22d3ee,#a78bfa,#22c55e);background-size:200% 200%;animation:gradientShift 3s ease infinite;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;margin-bottom:8px}
.hero-subtitle{color:#94a3b8;font-size:1.1rem;animation:fadeInUp 1s ease 0.3s both}
.metric-card{background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #1e3a5f;border-radius:20px;padding:24px 20px;text-align:center;animation:fadeInUp 0.6s ease both;transition:transform 0.3s ease,box-shadow 0.3s ease,border-color 0.3s ease;position:relative;overflow:hidden}
.metric-card::after{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.05),transparent);transition:left 0.5s ease}
.metric-card:hover::after{left:100%}.metric-card:hover{transform:translateY(-8px) scale(1.02);box-shadow:0 20px 60px rgba(34,211,238,0.15);border-color:#22d3ee}
.metric-icon{font-size:2.5rem;animation:float 3s ease infinite;display:block;margin-bottom:12px}
.metric-value{font-size:1.8rem;font-weight:700;color:#22d3ee;animation:countUp 0.8s ease both}
.metric-label{font-size:0.85rem;color:#64748b;font-weight:500;margin-top:4px}
.feature-card{background:#111827;border:1px solid #1f2937;border-radius:16px;padding:20px;margin:12px 0;animation:fadeInLeft 0.5s ease both;transition:all 0.3s ease}
.feature-card:hover{border-color:#22d3ee;transform:translateX(8px);box-shadow:-4px 0 20px rgba(34,211,238,0.2)}
.advice-card{background:linear-gradient(135deg,#0f2a1a,#111827);border-left:4px solid #22c55e;border-radius:0 12px 12px 0;padding:16px 20px;margin:10px 0;animation:slideInRight 0.5s ease both;transition:transform 0.2s ease}
.advice-card:hover{transform:scale(1.01)}
.warning-card{background:linear-gradient(135deg,#1c1a0a,#111827);border-left:4px solid #f59e0b;border-radius:0 12px 12px 0;padding:16px 20px;margin:10px 0;animation:slideInRight 0.5s ease both}
.danger-card{background:linear-gradient(135deg,#1c0a0a,#111827);border-left:4px solid #ef4444;border-radius:0 12px 12px 0;padding:16px 20px;margin:10px 0;animation:slideInRight 0.5s ease both}
.success-card{background:linear-gradient(135deg,#0a1c0f,#111827);border-left:4px solid #22c55e;border-radius:0 12px 12px 0;padding:16px 20px;margin:10px 0;animation:slideInRight 0.5s ease both}
.transaction-row{background:#111827;border:1px solid #1f2937;border-radius:12px;padding:14px 18px;margin:6px 0;animation:fadeInUp 0.4s ease both;transition:all 0.2s ease;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.transaction-row:hover{background:#1e293b;border-color:#334155;transform:translateX(4px)}
.badge{padding:4px 12px;border-radius:20px;font-size:0.75rem;font-weight:600}
.badge-food{background:#064e3b;color:#34d399}.badge-shopping{background:#312e81;color:#a78bfa}.badge-transport{background:#0c4a6e;color:#38bdf8}.badge-health{background:#7f1d1d;color:#f87171}.badge-savings{background:#14532d;color:#4ade80}.badge-entertainment{background:#4a1942;color:#e879f9}.badge-groceries{background:#1a3a1a;color:#86efac}.badge-utilities{background:#1a1a3a;color:#93c5fd}.badge-banking{background:#3a1a1a;color:#fca5a5}.badge-other{background:#1e293b;color:#94a3b8}
.personality-card{background:linear-gradient(135deg,#1a0f2e,#0f1a2e);border:2px solid #a78bfa;border-radius:20px;padding:32px;text-align:center;animation:fadeInUp 0.8s ease,borderFlow 4s linear infinite}
.personality-emoji{font-size:5rem;animation:float 3s ease infinite;display:block;margin-bottom:16px}
.personality-title{font-size:1.8rem;font-weight:700;background:linear-gradient(135deg,#22d3ee,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.score-container{text-align:center;animation:fadeInUp 0.8s ease;padding:40px}.score-number{font-size:6rem;font-weight:800;animation:countUp 1s ease,glowPulse 3s ease infinite;background:linear-gradient(135deg,#22d3ee,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.score-ring{width:200px;height:200px;border-radius:50%;border:8px solid #22d3ee;animation:borderFlow 4s linear infinite,pulse 2s ease infinite;display:flex;align-items:center;justify-content:center;margin:0 auto 24px}
.sip-result{background:linear-gradient(135deg,#0f2a1a,#0a1628);border:2px solid #22c55e;border-radius:20px;padding:32px;text-align:center;animation:fadeInUp 0.6s ease,pulse 3s ease infinite}
.sip-amount{font-size:3.5rem;font-weight:800;color:#22c55e;animation:countUp 1s ease,glowPulse 3s ease infinite}
.goal-card{background:#111827;border:1px solid #1f2937;border-radius:16px;padding:20px;margin:12px 0;animation:fadeInUp 0.5s ease both;transition:all 0.3s ease}.goal-card:hover{border-color:#a78bfa;box-shadow:0 8px 30px rgba(167,139,250,0.15);transform:translateY(-4px)}
.grade-box{background:#111827;border-radius:16px;padding:24px;text-align:center;animation:fadeInUp 0.6s ease both;transition:transform 0.3s ease;border:1px solid #1f2937}.grade-box:hover{transform:scale(1.05)}.grade-letter{font-size:3.5rem;font-weight:800;animation:countUp 0.8s ease}
.login-container{max-width:420px;margin:60px auto;background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;border-radius:24px;padding:48px 40px;animation:fadeInUp 0.8s ease;box-shadow:0 25px 60px rgba(0,0,0,0.5)}
.login-logo{font-size:4rem;text-align:center;animation:float 3s ease infinite;display:block;margin-bottom:8px}.login-title{font-size:2rem;font-weight:800;text-align:center;background:linear-gradient(135deg,#22d3ee,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:4px}.login-subtitle{text-align:center;color:#64748b;font-size:0.9rem;margin-bottom:32px}
.chat-container{max-height:400px;overflow-y:auto;padding:16px;background:#0a0f1a;border-radius:16px;border:1px solid #1e293b}.user-bubble{background:linear-gradient(135deg,#0284c7,#0369a1);color:white;border-radius:20px 20px 4px 20px;padding:14px 18px;margin:8px 0 8px auto;max-width:75%;width:fit-content;margin-left:auto;animation:slideInRight 0.3s ease;box-shadow:0 4px 15px rgba(2,132,199,0.3)}.ai-bubble{background:linear-gradient(135deg,#4c1d95,#6d28d9);color:white;border-radius:20px 20px 20px 4px;padding:14px 18px;margin:8px 0;max-width:75%;width:fit-content;animation:fadeInLeft 0.3s ease;box-shadow:0 4px 15px rgba(109,40,217,0.3)}
.anomaly-danger{background:linear-gradient(135deg,#1c0a0a,#111827);border:1px solid #ef4444;border-radius:12px;padding:16px 20px;margin:8px 0;animation:fadeInUp 0.5s ease,pulse 2s ease infinite}.anomaly-warning{background:linear-gradient(135deg,#1c1a0a,#111827);border:1px solid #f59e0b;border-radius:12px;padding:16px 20px;margin:8px 0;animation:fadeInUp 0.5s ease}
.custom-divider{height:1px;background:linear-gradient(90deg,transparent,#334155,transparent);margin:24px 0}.footer{text-align:center;color:#334155;font-size:0.8rem;padding:24px 0;border-top:1px solid #1e293b;margin-top:48px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f172a,#080c14) !important;border-right:1px solid #1e293b}section[data-testid="stSidebar"] .stRadio label{color:#94a3b8 !important;padding:8px 12px;border-radius:8px;transition:all 0.2s ease;display:block}section[data-testid="stSidebar"] .stRadio label:hover{background:#1e293b;color:#22d3ee !important}
.stButton>button{background:linear-gradient(135deg,#22d3ee,#a78bfa) !important;color:#0f172a !important;border:none !important;border-radius:12px !important;padding:12px 28px !important;font-weight:700 !important;font-size:0.95rem !important;transition:all 0.3s ease !important;box-shadow:0 4px 15px rgba(34,211,238,0.3) !important}.stButton>button:hover{transform:translateY(-3px) !important;box-shadow:0 8px 30px rgba(34,211,238,0.5) !important}
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:#1e293b !important;color:#f1f5f9 !important;border:1px solid #334155 !important;border-radius:10px !important;transition:border-color 0.3s ease !important}.stTextInput input:focus,.stNumberInput input:focus{border-color:#22d3ee !important;box-shadow:0 0 0 3px rgba(34,211,238,0.1) !important}.stSelectbox>div>div{background:#1e293b !important;border:1px solid #334155 !important;border-radius:10px !important;color:#f1f5f9 !important}
.stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:12px;padding:4px;gap:4px}.stTabs [data-baseweb="tab"]{background:transparent;color:#64748b;border-radius:8px;font-weight:600;transition:all 0.2s ease}.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#22d3ee,#a78bfa) !important;color:#0f172a !important}
[data-testid="stMetricValue"]{color:#22d3ee !important;font-size:2rem !important;font-weight:700 !important}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:#0f172a}::-webkit-scrollbar-thumb{background:linear-gradient(#22d3ee,#a78bfa);border-radius:3px}
.streamlit-expanderHeader{background:#111827 !important;border-radius:10px !important;color:#94a3b8 !important}thead tr th{background:#1e293b !important;color:#22d3ee !important}tbody tr:hover td{background:#1e293b !important}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "default"
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

MENU_LIST = [
    "🏠 Home",
    "📷 Upload Screenshot",
    "✏️ Manual Entry",
    "📊 Analysis",
    "💰 Budget Tracker",
    "📱 SMS Parser",
    "💯 Health Score",
    "🎯 Goals",
    "🔮 What If",
    "📚 Book Advisor",
    "🌟 Spending Personality",
    "📈 Report Card",
    "🇮🇳 Indian Finance",
    "🤖 Guru AI Chat",
    "👥 Splitwise",
    "📄 Export Report",
]
CATEGORIES = list(KEYWORDS.keys()) + ["Other", "Rent", "Travel", "Bills"]
CHART_COLORS = ["#22d3ee", "#a78bfa", "#22c55e", "#f59e0b", "#ef4444", "#f472b6"]


def money(amount):
    return f"₹{float(amount or 0):,.2f}"


def username():
    return st.session_state.get("username", "default")


def render_page_header(title, subtitle):
    st.markdown(f"""
    <div class="hero-banner">
      <div class="hero-title">{title}</div>
      <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="custom-divider"></div>
    <div class="footer">
      💰 FinanceAI • Made for India • Educational only • Not financial advice
    </div>
    """, unsafe_allow_html=True)


def card(text, kind="feature"):
    st.markdown(f"<div class=\"{kind}-card\">{text}</div>", unsafe_allow_html=True)


def metric_card(column, icon, label, value):
    column.markdown(f"""
    <div class="metric-card">
      <span class="metric-icon">{icon}</span>
      <div class="metric-value">{value}</div>
      <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_plotly(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#080c14",
        plot_bgcolor="#111827",
        font=dict(color="#e2e8f0"),
        colorway=CHART_COLORS,
    )
    st.plotly_chart(fig, use_container_width=True)


def badge_class(category):
    return f"badge-{str(category or 'Other').lower()}"


def get_this_month_total(user):
    current_month = datetime.now().strftime("%Y-%m")
    return sum(
        float(e.get("amount", 0))
        for e in load_expenses(user)
        if str(e.get("date", "")).startswith(current_month)
    )


def login_page():
    st.markdown("""
    <div class="login-container">
      <span class="login-logo">💰</span>
      <div class="login-title">FinanceAI</div>
      <div class="login-subtitle">Your Smart Indian Money Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    user = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    if st.button("Login →", use_container_width=True):
        if verify_login(user, password):
            st.session_state.logged_in = True
            st.session_state.username = user
            user_data_dir(user)
            st.rerun()
        else:
            st.markdown("""
            <div class="danger-card">❌ Wrong username or password</div>
            """, unsafe_allow_html=True)


if not st.session_state.get("logged_in") or "username" not in st.session_state:
    login_page()
    st.stop()


def get_current_data():
    expenses = load_expenses(username())
    goals = load_goals(username())
    total, category_data, monthly_data = analyze(expenses)
    return expenses, goals, total, category_data, monthly_data


def spending_context(expenses):
    total, category_data, _monthly_data = analyze(expenses)
    top = top_category(category_data)
    breakdown = ", ".join(f"{category}: {money(amount)}" for category, amount in category_data.items())
    return total, category_data, top, breakdown or "No category spending yet"


def render_anomalies(expenses):
    anomalies = detect_anomalies(expenses)
    if not anomalies:
        card("✅ No unusual weekly spending spikes detected.", "success")
        return
    for item in anomalies:
        cls = "anomaly-danger" if item["alert_level"] == "danger" else "anomaly-warning"
        st.markdown(f"""
        <div class="{cls}">
          ⚠️ <b>{item['category']}</b>: {item['message']}
          <br>Recent {money(item['recent_weekly'])} vs usual {money(item['usual_weekly'])}
        </div>
        """, unsafe_allow_html=True)


def render_personality(total, category_data):
    savings = sum(float(v or 0) for k, v in category_data.items() if str(k).lower() == "savings")
    savings_rate = savings / total * 100 if total else 0
    profile = get_spending_personality(total, category_data, savings_rate)
    st.markdown(f"""
    <div class="personality-card">
      <span class="personality-emoji">{profile['emoji']}</span>
      <div class="personality-title">{profile['title']}</div>
      <p>{profile['description']}</p>
      <p><b>Strength:</b> {profile['strength']} &nbsp; <b>Watch:</b> {profile['weakness']}</p>
      <p><b>Tip:</b> {profile['tip']}</p>
      <p>{profile['celebrity_match']}</p>
    </div>
    """, unsafe_allow_html=True)


def navigate(page):
    st.session_state.page = page
    st.session_state.main_menu = page
    st.rerun()


def dashboard():
    render_page_header("🏠 FinanceAI Dashboard", "Your money, goals, alerts, and next best actions in one place")
    expenses, goals, total, category_data, _monthly_data = get_current_data()
    current_month = datetime.now().strftime("%Y-%m")
    month_expenses = [e for e in expenses if str(e.get("date", "")).startswith(current_month)]
    month_total, month_categories, _ = analyze(month_expenses)
    budget_limit = float(st.session_state.get("monthly_budget", 0.0))
    health = calculate_health_score(month_total, month_categories, goals, budget_limit)

    c1, c2, c3, c4 = st.columns(4)
    metric_card(c1, "💸", "This Month", money(month_total))
    metric_card(c2, "📊", "Budget Used", f"{(month_total / budget_limit * 100):.1f}%" if budget_limit else "Set budget")
    metric_card(c3, "🏷️", "Top Category", top_category(month_categories or category_data))
    metric_card(c4, "💯", "Health Score", f"{health['score']} {health['grade']}")

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    if expenses:
        render_personality(total, category_data)
    else:
        card("Add your first expense to reveal your spending personality.", "feature")

    st.subheader("🚨 Anomaly Alerts")
    render_anomalies(expenses)

    st.subheader("🧾 Recent Transactions")
    recent = list(reversed(expenses[-5:]))
    if recent:
        for item in recent:
            category = item.get("category", "Other")
            st.markdown(f"""
            <div class="transaction-row">
              <div><b>{item.get('merchant', 'Unknown')}</b><br><span style="color:#64748b">{item.get('date', '')}</span></div>
              <div><span class="badge {badge_class(category)}">{category}</span></div>
              <div style="color:#22d3ee;font-weight:700">{money(item.get('amount', 0))}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        card("No transactions yet. Add an expense, scan a receipt, or parse bank SMS.", "feature")


def upload_screenshot():
    render_page_header("📷 Scan Receipt", "Upload any UPI or payment screenshot")
    file = st.file_uploader("", type=["png", "jpg", "jpeg"], help="Supports PhonePe, GPay, Paytm, bank receipts")
    if file is None:
        return

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(file, caption="Uploaded", use_container_width=True)
    with col2:
        with st.spinner("🔍 Reading receipt..."):
            file.seek(0)
            text, _ = extract_text_and_amount(file)
            file.seek(0)
            merchant, amount, currency = extract_details(text)
            category = categorize(text)

        if text:
            st.markdown(f"""
            <div class="feature-card">
              <div style="color:#64748b;font-size:0.8rem">EXTRACTED TEXT</div>
              <div style="color:#94a3b8;font-size:0.85rem;margin-top:8px">{text[:200]}...</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="feature-card">
              <div>🏪 <b>Merchant:</b> <span style="color:#22d3ee">{merchant}</span></div>
              <div style="margin-top:8px">💰 <b>Amount:</b> <span style="color:#22c55e;font-size:1.2rem;font-weight:700">{currency}{amount}</span></div>
              <div style="margin-top:8px">🏷️ <b>Category:</b> <span class="badge {badge_class(category)}">{category}</span></div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("✏️ Edit Before Saving")
            edit_amount = st.number_input("Amount", value=float(amount) if amount > 0 else 0.0, min_value=0.0)
            cats = ["Food", "Shopping", "Transport", "Entertainment", "Health", "Banking", "Groceries", "Utilities", "Savings", "Other"]
            edit_cat = st.selectbox("Category", cats, index=cats.index(category) if category in cats else 0)
            edit_merchant = st.text_input("Merchant", value=merchant)
            if st.button("💾 Save Expense", use_container_width=True):
                if edit_amount > 0:
                    save_expense(edit_amount, edit_cat, edit_merchant, username())
                    st.success("✅ Saved!")
                    st.balloons()
                else:
                    st.error("❌ Enter valid amount")
        else:
            st.markdown("""<div class="danger-card">❌ Could not read image. Try clearer photo.</div>""", unsafe_allow_html=True)


def manual_entry():
    render_page_header("✏️ Manual Entry", "Add a transaction in seconds")
    with st.form("manual_entry_form"):
        amount = st.number_input("Amount", min_value=0.0, step=10.0)
        category = st.selectbox("Category", CATEGORIES)
        merchant = st.text_input("Merchant", value="Unknown")
        submitted = st.form_submit_button("💾 Save Expense", use_container_width=True)
    if submitted:
        save_expense(amount, category, merchant, username())
        st.markdown("""<div class="success-card">✅ Expense saved successfully.</div>""", unsafe_allow_html=True)


def csv_upload():
    render_page_header("📥 CSV Upload", "Bulk import expenses from a CSV")
    csv_file = st.file_uploader("Upload CSV with amount, category columns", type=["csv"])
    if not csv_file:
        return
    try:
        df = pd.read_csv(csv_file)
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        return
    st.dataframe(df.head(20), use_container_width=True)
    required = {"amount", "category"}
    if not required.issubset({col.lower() for col in df.columns}):
        st.error("CSV must include amount and category columns.")
        return
    columns = {col.lower(): col for col in df.columns}
    if st.button("Import CSV", type="primary"):
        rows = []
        for _, row in df.iterrows():
            rows.append({
                "amount": row[columns["amount"]],
                "category": row[columns["category"]],
                "merchant": row[columns["merchant"]] if "merchant" in columns else "CSV Import",
                "date": row[columns["date"]] if "date" in columns else datetime.now().strftime("%Y-%m-%d"),
            })
        imported = save_many_expenses(rows, username())
        st.success(f"Imported {len(imported)} expenses.")


def analysis_page():
    render_page_header("📊 Analysis", "Understand your categories, trends, and spending signals")
    expenses, _goals, total, category_data, monthly_data = get_current_data()
    c1, c2, c3 = st.columns(3)
    metric_card(c1, "💰", "Total Spend", money(total))
    metric_card(c2, "🧮", "Categories", len(category_data))
    metric_card(c3, "🏆", "Top Category", top_category(category_data))
    render_anomalies(expenses)
    if category_data:
        cat_df = pd.DataFrame({"Category": category_data.keys(), "Amount": category_data.values()})
        render_plotly(px.pie(cat_df, names="Category", values="Amount", title="Spend Mix", color_discrete_sequence=CHART_COLORS))
        render_plotly(px.bar(cat_df, x="Category", y="Amount", title="Category Spend", color="Category", color_discrete_sequence=CHART_COLORS))
    if monthly_data:
        month_df = pd.DataFrame({"Month": monthly_data.keys(), "Amount": monthly_data.values()}).sort_values("Month")
        render_plotly(px.line(month_df, x="Month", y="Amount", markers=True, title="Monthly Trend"))
    for item in spending_insights(total, category_data):
        kind = "warning" if "high" in item.lower() else "advice"
        card(item, kind)
    card(f"Monthly trend: {monthly_trend(monthly_data)}", "feature")
    st.metric("Predicted Monthly Spend", money(predict_monthly_spending(username())))


def budget_tracker():
    render_page_header("💰 Budget Tracker", "Track budget usage before it tracks you")
    current_budget = float(st.session_state.get("monthly_budget", 0.0))
    budget = st.number_input("Monthly budget", min_value=0.0, value=current_budget, step=500.0)
    if st.button("Set Budget", use_container_width=True):
        st.session_state["monthly_budget"] = budget
        st.success(f"Budget set to {money(budget)}.")
    month_total = get_this_month_total(username())
    remaining = budget - month_total
    c1, c2 = st.columns(2)
    metric_card(c1, "💸", "Spent", money(month_total))
    metric_card(c2, "🧘", "Remaining", money(remaining))
    if budget:
        usage = month_total / budget
        color = "#22c55e" if usage < 0.6 else "#f59e0b" if usage <= 0.8 else "#ef4444"
        st.markdown(f"""
        <div style="background:#111827;border-radius:999px;height:28px;overflow:hidden;border:1px solid #1f2937">
          <div style="height:100%;width:{min(usage,1)*100:.1f}%;background:{color};border-radius:999px"></div>
        </div>
        <p style="color:#94a3b8">{usage*100:.1f}% used</p>
        """, unsafe_allow_html=True)
        if usage > 1:
            card("🚨 Budget exceeded. Pause non-essential spending.", "danger")
        elif usage > 0.8:
            card("⚠️ You have used more than 80% of your budget.", "warning")
        else:
            card("✅ Budget is under control.", "success")
    month_expenses = [e for e in load_expenses(username()) if str(e.get("date", "")).startswith(datetime.now().strftime("%Y-%m"))]
    spent, category_data, _ = analyze(month_expenses)
    for insight in rule_budget_analysis(spent, category_data):
        card(insight, "warning" if "⚠" in insight else "advice")


def sms_parser_page():
    render_page_header("📱 SMS Parser", "Turn Indian bank alerts into clean expense rows")
    placeholder = "Dear Customer, Rs.500.00 debited from ac XXXX for UPI/Zomato\nHDFC Bank: INR 1,200 spent on Amazon on 12-Jun-26\nSBI: Your a/c debited by Rs 340 on 12/06/26 trf to Swiggy\nPaytm: Payment of ₹450 to Dominos successful"
    text = st.text_area("Paste your bank SMS messages here (one per line)", placeholder=placeholder, height=180)
    if st.button("Parse SMS", use_container_width=True):
        st.session_state["parsed_sms"] = parse_multiple_sms(text)
        st.session_state["sms_total_lines"] = len([line for line in text.splitlines() if line.strip()])
    parsed = st.session_state.get("parsed_sms", [])
    if parsed:
        card(f"Found {len(parsed)} transactions from {st.session_state.get('sms_total_lines', len(parsed))} SMS messages.", "success")
        st.dataframe(pd.DataFrame(parsed)[["amount", "merchant", "transaction_type", "bank"]], use_container_width=True, hide_index=True)
        selected = []
        for idx, item in enumerate(parsed):
            if st.checkbox(f"Save {money(item['amount'])} - {item['merchant']}", value=True, key=f"sms_{idx}"):
                selected.append(item)
        if st.button("Save Selected", use_container_width=True):
            for item in selected:
                save_expense(item["amount"], categorize(item["merchant"]), item["merchant"], username())
            st.success(f"Saved {len(selected)} transactions.")


def health_score_page():
    render_page_header("💯 Health Score", "A quick pulse check for your financial habits")
    _expenses, goals, total, category_data, _monthly_data = get_current_data()
    health = calculate_health_score(total, category_data, goals, float(st.session_state.get("monthly_budget", 0.0)))
    st.markdown(f"""
    <div class="score-container">
      <div class="score-ring"><div class="score-number">{health['score']}</div></div>
      <h2>{health['grade']} • {health['label']}</h2>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(4)
    breakdown = health["breakdown"]
    for col, (label, value, max_value) in zip(cols, [
        ("Savings", breakdown["savings_score"], 30),
        ("Spending", breakdown["spending_score"], 30),
        ("Budget", breakdown["budget_score"], 20),
        ("Goals", breakdown["goals_score"], 20),
    ]):
        with col:
            card(f"<b>{label}</b><br>{value}/{max_value}", "feature")
            st.progress(min(value / max_value, 1.0))
    for tip in health["tips"]:
        card(tip, "advice")
    better = 85 if health["score"] > 80 else 60 if health["score"] > 60 else 40
    card(f"Better than {better}% of savers.", "success")


def goals_page():
    render_page_header("🎯 Goals", "Give your savings a destination")
    goals = load_goals(username())
    with st.form("goal_form"):
        name = st.text_input("Goal name")
        target = st.number_input("Target amount", min_value=0.0, step=1000.0)
        monthly_saving = st.number_input("Monthly saving", min_value=0.0, step=500.0)
        submitted = st.form_submit_button("Add Goal", use_container_width=True)
    if submitted and name:
        save_goal(name, target, monthly_saving, username())
        st.success("Goal added.")
        st.rerun()
    for goal in goals:
        months = months_to_goal(goal.get("target"), goal.get("monthly_saving"))
        st.markdown(f"""
        <div class="goal-card">
          <h3>{goal.get('name', 'Goal')}</h3>
          <p>Target {money(goal.get('target'))} • Monthly {money(goal.get('monthly_saving'))} • {months} months</p>
        </div>
        """, unsafe_allow_html=True)
        monthly = float(goal.get("monthly_saving", 0) or 0)
        target = float(goal.get("target", 1) or 1)
        st.progress(min(monthly / target, 1.0))
        if st.button("Delete", key=f"delete_{goal.get('id')}"):
            delete_goal(goal.get("id"), username())
            st.rerun()


def what_if_page():
    render_page_header("🔮 What If", "Simulate small changes before making them")
    _expenses, _goals, total, category_data, _monthly_data = get_current_data()
    st.subheader("What if I save more?")
    extra = st.slider("Extra monthly saving", 500, 10000, 2000, 500)
    years = st.slider("Years", 1, 10, 5)
    result = simulate_savings(total, extra, years)
    st.markdown(f"<div class='sip-result'><div class='sip-amount'>{money(result['with_interest'])}</div><p>Estimated maturity</p></div>", unsafe_allow_html=True)
    card("🎁 You could buy: " + (", ".join(result["what_you_can_buy"]) if result["what_you_can_buy"] else "Keep compounding for bigger goals"), "success")
    st.subheader("What if I cut spending?")
    category = st.selectbox("Category", list(category_data.keys()) or ["Food"])
    cut = st.slider("Cut by", 10, 50, 20)
    cut_result = simulate_cut_spending(category, category_data.get(category, 0), cut)
    c1, c2, c3 = st.columns(3)
    metric_card(c1, "📆", "Monthly Saving", money(cut_result["monthly_saving"]))
    metric_card(c2, "🗓️", "Yearly Saving", money(cut_result["yearly_saving"]))
    metric_card(c3, "📈", "5Y Value", money(cut_result["five_year_value"]))
    st.subheader("What if I started SIP earlier?")
    sip_df = pd.DataFrame([
        {"Scenario": "Started 1yr ago", "Value": sip_calculator(extra, 12, years + 1)},
        {"Scenario": "Start now", "Value": sip_calculator(extra, 12, years)},
        {"Scenario": "Start 1yr later", "Value": sip_calculator(extra, 12, max(years - 1, 1))},
    ])
    st.dataframe(sip_df, use_container_width=True, hide_index=True)


def book_advisor_page():
    render_page_header("📚 Book Advisor", "Apply financial books to your real spending")
    show_book_advisor()


def personality_page():
    render_page_header("🌟 Spending Personality", "Your money habits, but make them readable")
    _expenses, _goals, total, category_data, _monthly_data = get_current_data()
    if total <= 0:
        card("Add expenses to reveal your spending personality.", "feature")
        return
    render_personality(total, category_data)


def report_card_page():
    render_page_header("📈 Report Card", "A school-style monthly review for your money")
    expenses, goals, _total, _category_data, _monthly_data = get_current_data()
    report = generate_report_card(expenses, float(st.session_state.get("monthly_budget", 0.0)), goals)
    st.markdown(f"<h1 style='text-align:center'>Overall Grade: {report['overall']}</h1>", unsafe_allow_html=True)
    cols = st.columns(4)
    for col, (name, grade) in zip(cols, report["grades"].items()):
        col.markdown(f"<div class='grade-box'><div class='grade-letter'>{grade}</div><p>{name}</p></div>", unsafe_allow_html=True)
    comparison = report["comparison"]
    arrow = "⬆️" if comparison["direction"] == "up" else "⬇️" if comparison["direction"] == "down" else "➡️"
    card(f"{arrow} Compared to last month: {money(comparison['change'])}", "warning" if comparison["direction"] == "up" else "success")
    for insight in report["insights"]:
        card(insight, "advice")
    summary = f"FinanceAI Report Card: Overall {report['overall']}, current spend {money(comparison['current'])}, previous {money(comparison['previous'])}."
    if st.button("Share Report", use_container_width=True):
        st.code(summary)
        st.caption("Copy this summary to share.")


def indian_finance_page():
    render_page_header("🇮🇳 Indian Finance", "SIP, tax saving, and Indian investment comparisons")
    _expenses, _goals, total, category_data, _monthly_data = get_current_data()
    c1, c2, c3 = st.columns(3)
    monthly = c1.number_input("Monthly SIP", min_value=0.0, value=5000.0, step=500.0)
    rate = c2.number_input("Annual return %", min_value=0.0, value=12.0, step=0.5)
    years = c3.number_input("Years", min_value=1, value=10, step=1)
    st.markdown(f"<div class='sip-result'><div class='sip-amount'>{money(sip_calculator(monthly, rate, years))}</div><p>Estimated SIP maturity</p></div>", unsafe_allow_html=True)
    income = st.number_input("Annual income", min_value=0.0, value=600000.0, step=50000.0)
    for tip in tax_saving_tips(income, category_data):
        card(tip, "advice")
    compare_df = pd.DataFrame([{"Option": name, "Rate %": item["rate"], "5Y Value": item["value"]} for name, item in compare_investments().items()])
    st.dataframe(compare_df, use_container_width=True, hide_index=True)
    status = check_50_30_20(total, category_data)
    card(f"Needs: {status['needs_%']:.1f}% | Wants: {status['wants_%']:.1f}% | Savings: {status['savings_%']:.1f}%", "success")


def guru_chat():
    st.subheader("🧙 Guru AI – Your Financial Advisor")

    import google.generativeai as genai

    key = st.secrets.get("GEMINI_API_KEY", "")
    if not key:
        st.error("GEMINI_API_KEY not found in secrets")
        return

    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    if "guru_messages" not in st.session_state:
        st.session_state.guru_messages = []

    for msg in st.session_state.guru_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask Guru about money, savings, investments...")
    if user_input:
        st.session_state.guru_messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        history = [
            {
                "role": "user",
                "parts": [
                    "You are Guru, a friendly Indian personal finance advisor. "
                    "Give practical advice for Indian users about SIP, PPF, ELSS, "
                    "NPS, 80C tax saving, UPI budgeting and EMI management. "
                    "Be concise and warm. Remind users you are an AI not a SEBI advisor."
                ]
            },
            {
                "role": "model",
                "parts": ["Understood! I am Guru, your Indian finance advisor. How can I help?"]
            }
        ]

        for msg in st.session_state.guru_messages[:-1]:
            role = "model" if msg["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [msg["content"]]})

        try:
            chat = model.start_chat(history=history)
            response = chat.send_message(user_input)
            reply = response.text
        except Exception as e:
            reply = f"Error: {e}"

        st.session_state.guru_messages.append(
            {"role": "assistant", "content": reply}
        )
        with st.chat_message("assistant"):
            st.markdown(reply)


def splitwise_page():
    render_page_header("👥 Splitwise", "Split bills cleanly")
    total_bill = st.number_input("Total bill", min_value=0.0, step=100.0)
    people = st.number_input("Number of people", min_value=1, value=2, step=1)
    add_names = st.checkbox("Add names")
    names = [st.text_input(f"Person {i + 1}", value=f"Person {i + 1}") for i in range(int(people))] if add_names else []
    share = total_bill / people if people else 0
    st.metric("Each person's share", money(share))
    if names:
        st.dataframe(pd.DataFrame({"Name": names, "Share": [money(share)] * len(names)}), hide_index=True)


def export_report_page():
    render_page_header("📄 Export Report", "Download a PDF summary of your finances")
    _expenses, _goals, total, category_data, monthly_data = get_current_data()
    advice_list = give_advice(total, category_data, username())
    budget_insights = rule_budget_analysis(total, category_data)
    card(f"Total spending: <b>{money(total)}</b>", "feature")
    if st.button("Generate PDF", use_container_width=True):
        with st.spinner("Generating PDF..."):
            pdf_bytes = generate_pdf_report(total, category_data, monthly_data, advice_list, budget_insights)
        st.download_button("Download Financial Report", data=pdf_bytes, file_name=f"financial_report_{datetime.now().strftime('%Y_%m')}.pdf", mime="application/pdf")


PAGES = {
    "🏠 Home": dashboard,
    "📷 Upload Screenshot": upload_screenshot,
    "✏️ Manual Entry": manual_entry,
    "📊 Analysis": analysis_page,
    "💰 Budget Tracker": budget_tracker,
    "📱 SMS Parser": sms_parser_page,
    "💯 Health Score": health_score_page,
    "🎯 Goals": goals_page,
    "🔮 What If": what_if_page,
    "📚 Book Advisor": book_advisor_page,
    "🌟 Spending Personality": personality_page,
    "📈 Report Card": report_card_page,
    "🇮🇳 Indian Finance": indian_finance_page,
    "🤖 Guru AI Chat": guru_chat,
    "👥 Splitwise": splitwise_page,
    "📄 Export Report": export_report_page,
}


def main():
    user = username()
    total_this_month = get_this_month_total(user)
    if st.session_state.get("main_menu") in MENU_LIST and st.session_state.main_menu != st.session_state.page:
        st.session_state.page = st.session_state.main_menu

    st.sidebar.markdown(f"""
    <div style="padding:16px;background:#111827;border-radius:12px;margin-bottom:16px;border:1px solid #1e293b;text-align:center">
      <div style="font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#22d3ee,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">💰 FinanceAI</div>
      <div style="color:#475569;font-size:0.75rem">Smart Money Assistant</div>
    </div>
    <div style="padding:10px 12px;background:#111827;border-radius:10px;margin-bottom:8px;border:1px solid #1e293b">
      <div style="color:#64748b;font-size:0.7rem">LOGGED IN AS</div>
      <div style="color:#22d3ee;font-weight:600">👤 {user}</div>
    </div>
    <div style="padding:10px 12px;background:#111827;border-radius:10px;margin-bottom:16px;border:1px solid #1e293b">
      <div style="color:#64748b;font-size:0.7rem">THIS MONTH</div>
      <div style="color:#f1f5f9;font-weight:700;font-size:1.1rem">₹{total_this_month:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio(
        "",
        MENU_LIST,
        index=MENU_LIST.index(st.session_state.page) if st.session_state.page in MENU_LIST else 0,
        key="main_menu",
    )
    st.session_state.page = menu
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.sidebar.caption("Made with ❤️ for India")

    PAGES[menu]()
    render_footer()


if __name__ == "__main__":
    main()
