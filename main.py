import streamlit as st
import requests
import uuid

# ----------------------------------------------------------------
# 🚀 App Setup
# ----------------------------------------------------------------

st.set_page_config(
    page_title="RiskGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

API_URL = st.secrets["API_URL"]
CHAT_URL = st.secrets["CHAT_URL"]

# ----------------------------------------------------------------
# 🎨 Styling
# ----------------------------------------------------------------

st.markdown("""
<style>

body {
    font-family: 'Segoe UI', sans-serif;
}

/* Headings */
h1, .section-title {
    color: #1f2c3a;
    font-weight: 600;
}

/* Rounded card styling */
.card {
    background: #f8fafc;
    padding: 18px;
    border-radius: 10px;
    margin: 12px 0;
    border: 1px solid #e9edf3;
}

/* Advisor text box */
.advisor-box {
    background: #eef7ff;
    border-left: 4px solid #2980b9;
    padding: 16px;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 15px;
}

/* Chat bubbles */
.chat-user {
    background:#dff9fb;
    padding:10px;
    border-radius:8px;
    margin:6px 0;
    text-align:right;
    font-size:14px;
}

.chat-bot {
    background:#f4f9ff;
    border-left:4px solid #2980b9;
    padding:10px;
    border-radius:8px;
    margin:6px 0;
    font-size:14px;
}

/* Sidebar Chat container */
.chat-box {
    height:350px;
    overflow-y:auto;
    background:#fafafa;
    border:1px solid #ddd;
    border-radius:8px;
    padding:10px;
}

/* Buttons */
.stButton>button {
    background:#1f77ff;
    color:white;
    border-radius:6px;
    font-weight:600;
    height:45px;
}

.stButton>button:hover {
    background:#1453cc;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------
# 🧠 Sidebar Chatbot
# ----------------------------------------------------------------

with st.sidebar:
    st.markdown("## 💬 Chat With RiskGuard AI")
    st.markdown("""
        <small style='color:#6c757d;'>Ask questions about your loan approval, score improvement, risk factors and eligibility.</small>
        <hr>
    """, unsafe_allow_html=True)

    chat_box = st.container()

    with chat_box:
        st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

        for role, msg in st.session_state.chat_history:
            bubble = "chat-user" if role == "user" else "chat-bot"
            st.markdown(f"<div class='{bubble}'>{msg}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    user_message = st.text_input(
        "Type your question...", 
        placeholder="Example: How can I get approved next time?",
        disabled=not st.session_state.analysis_done
    )

    if st.button("Send", use_container_width=True) and user_message.strip():
        payload = {
            "thread_id": st.session_state.thread_id,
            "message": user_message
        }
        
        try:
            res = requests.post(CHAT_URL, json=payload).json()
            reply = res.get("response", "⚠️ No response received.")

            st.session_state.chat_history.append(("user", user_message))
            st.session_state.chat_history.append(("bot", reply))

        except Exception:
            st.error("⚠️ Chat server unavailable.")


# ----------------------------------------------------------------
# 🏦 Main App Content
# ----------------------------------------------------------------

st.title("🛡️ RiskGuard AI: Credit Risk Modelling")
st.write("A smart AI assistant that analyzes loan eligibility and explains financial decisions.")

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 18, 100, 28)
    income = st.number_input("Annual Income (₹)", 0, 30000000, 900000)
    loan_amount = st.number_input("Loan Amount (₹)", 0, 20000000, 2500000)
    loan_tenure_months = st.number_input("Loan Tenure (Months)", 1, 360, 36)
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])

with col2:
    loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
    loan_purpose = st.selectbox("Loan Purpose", ["Home", "Auto", "Business", "Personal", "Education"])
    avg_dpd_per_delinquency = st.number_input("Avg Days Past Due", 0, 200, 10)
    delinquency_ratio = st.slider("Delinquency Ratio (%)", 0, 100, 30)
    credit_utilization_ratio = st.slider("Credit Utilization (%)", 0, 100, 40)
    num_open_accounts = st.number_input("Active Loan Accounts", 1, 10, 2)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 🧮 Submit
# ----------------------------------------------------------------

if st.button("🔍 Analyze Credit Risk", use_container_width=True):
    
    payload = {
        "age": age,
        "income": income,
        "loan_amount": loan_amount,
        "loan_tenure_months": loan_tenure_months,
        "avg_dpd_per_delinquency": avg_dpd_per_delinquency,
        "delinquency_ratio": delinquency_ratio,
        "credit_utilization_ratio": credit_utilization_ratio,
        "num_open_accounts": num_open_accounts,
        "residence_type": residence_type,
        "loan_purpose": loan_purpose,
        "loan_type": loan_type,
    }

    with st.spinner("Evaluating your financial profile..."):
        result = requests.post(API_URL, json=payload).json()

    st.subheader("📊 Credit Assessment Report")

    st.markdown(f"""
    <div class="card">
        <b>Credit Score:</b> {result['credit_score']}<br>
        <b>Default Risk:</b> {result['probability']:.2%}<br>
        <b>Rating:</b> {result['rating']}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🤖 AI Advisor Insights")
    st.markdown(f"<div class='advisor-box'>{result['advisor_response']}</div>", unsafe_allow_html=True)

    st.session_state.analysis_done = True
    st.success("🎉 Analysis complete. You can now chat with the advisor in the sidebar!")


