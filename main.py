import streamlit as st
import requests
import uuid

# Page configuration
st.set_page_config(
    page_title="RiskGuard AI: Credit Risk Modelling",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# -------------------- SIDEBAR CHATBOT --------------------

with st.sidebar:
    st.markdown("""
        <h3 style='color:#2c3e50; margin-bottom:5px;'>💬 RiskGuard AI Assistant</h3>
        <p style='font-size:13px; color:#7f8c8d;'>
            Ask follow-up questions about your loan eligibility, credit score or improvement strategy.
        </p>
        <hr style='margin:10px 0;'>
    """, unsafe_allow_html=True)

    CHAT_URL = st.secrets["CHAT_URL"]

    # Show previous messages
    chat_container = st.container(height=350)

    with chat_container:
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"""
                <div style='background:#dff9fb; padding:8px; border-radius:6px; margin:5px; text-align:right;'>
                    {msg}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background:#f4f9ff; border-left:4px solid #2980b9; padding:8px; border-radius:6px; margin:5px;'>
                    {msg}
                </div>
                """, unsafe_allow_html=True)

    # Chat input
    user_msg = st.text_input("Type your message...", disabled=not st.session_state.analysis_done)

    send_button = st.button("Send", use_container_width=True, disabled=not st.session_state.analysis_done)

    if send_button and user_msg.strip():
        payload = {
            "thread_id": st.session_state.thread_id,
            "message": user_msg
        }

        try:
            response = requests.post(CHAT_URL, json=payload)
            reply = response.json().get("response", "⚠️ Bot did not respond.")

            st.session_state.chat_history.append(("user", user_msg))
            st.session_state.chat_history.append(("bot", reply))

        except:
            st.error("Chat server unavailable.")

# -------------------- MAIN PAGE UI --------------------

st.markdown("""
<style>
.result-box {
    background: #eef2f3;
    padding: 10px;
    border-radius: 6px;
    margin: 10px 0;
}
.advisor-box {
    background: #f7fbff;
    border-left: 4px solid #3498db;
    padding: 15px;
    border-radius: 6px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ RiskGuard AI")
st.write("Smart and AI-powered loan risk evaluation.")

# Inputs
age = st.number_input("Age", 18, 100, 30)
income = st.number_input("Annual Income (₹)", 0, 20000000, 1200000)
loan_amount = st.number_input("Loan Amount (₹)", 0, 20000000, 2500000)
loan_tenure_months = st.number_input("Loan Tenure (Months)", 1, 360, 36)
loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
loan_purpose = st.selectbox("Loan Purpose", ["Home", "Auto", "Business", "Personal", "Education"])
residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])

avg_dpd_per_delinquency = st.number_input("Avg Days Past Due", 0, 200, 10)
delinquency_ratio = st.slider("Delinquency Ratio (%)", 0, 100, 30)
credit_utilization_ratio = st.slider("Credit Utilization (%)", 0, 100, 40)
num_open_accounts = st.number_input("Active Loan Accounts", 1, 10, 2)


if st.button("🔍 Analyze Credit Risk", use_container_width=True):
    API_URL = st.secrets["API_URL"]

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
        "loan_type": loan_type
    }

    with st.spinner("Analyzing your financial profile..."):
        result = requests.post(API_URL, json=payload).json()

    st.markdown("### 📊 Assessment Summary")

    st.markdown(f"""
    <div class="result-box">
        <b>Credit Score:</b> {result['credit_score']} <br>
        <b>Default Risk:</b> {result['probability']:.2%} <br>
        <b>Rating:</b> {result['rating']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🤖 Advisor Response")

    st.markdown(f"""
    <div class="advisor-box">
        {result['advisor_response']}
    </div>
    """, unsafe_allow_html=True)

    st.session_state.analysis_done = True
