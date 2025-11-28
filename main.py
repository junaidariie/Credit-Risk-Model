import streamlit as st
import requests
import uuid

# Page configuration
st.set_page_config(
    page_title="RiskGuard AI: Credit Risk Modelling",
    page_icon="🛡️",
    layout="centered"
)

# Initialize session storage for chat messages and state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# ========================= UI STYLING =========================
st.markdown("""
<style>
.main { max-width: 800px; margin: 0 auto; }

.section-title {
    color: #34495e;
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 1.2rem;
}

.chat-bubble-user {
    background: #dff9fb;
    padding: 10px;
    border-radius: 8px;
    margin: 6px 0;
    text-align: right;
    font-size: 0.9rem;
}

.chat-bubble-bot {
    background: #eef5ff;
    border-left: 4px solid #2980b9;
    padding: 10px;
    border-radius: 8px;
    margin: 6px 0;
    font-size: 0.9rem;
}

.result-card {
    background: #ecf0f1;
    padding: 1.2rem;
    border-radius: 8px;
    margin-top: 1rem;
}

.stButton>button {
    width: 100%;
    background: #3498db;
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 0.6rem;
}
.stButton>button:hover { background: #2980b9; }

.advisor-box {
    background: #f4f9ff;
    border-left: 4px solid #2980b9;
    padding: 15px;
    margin-top: 15px;
    border-radius: 6px;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# ========================= HEADER =========================
st.title("🛡️ RiskGuard AI")
st.markdown("<p style='color:#7f8c8d;'>Advanced AI-Powered Credit Risk Assessment Platform</p>", unsafe_allow_html=True)
st.markdown("<p style='color:#4169e1'>⚠️ First request may take up to 20 seconds (API cold start).</p>", unsafe_allow_html=True)

# ========================= INPUT FORM =========================
st.markdown('<div class="section-title">Personal & Loan Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 18, 100, 28)
    loan_amount = st.number_input("Loan Amount (₹)", 0, 50000000, 2500000, step=100000)
    loan_purpose = st.selectbox("Loan Purpose", ["Education", "Home", "Auto", "Personal"])
with col2:
    income = st.number_input("Annual Income (₹)", 0, 50000000, 1200000, step=50000)
    loan_tenure_months = st.number_input("Loan Tenure (months)", 0, 480, 36)
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])

loan_to_income_ratio = loan_amount / income if income > 0 else 0
st.write(f"📊 **Loan-to-Income Ratio:** `{loan_to_income_ratio:.2f}`")

st.markdown('<div class="section-title">Credit Profile</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    avg_dpd_per_delinquency = st.number_input("Avg Days Past Due", 0, 200, 20)
    credit_utilization_ratio = st.number_input("Credit Utilization (%)", 0, 100, 30)
with col4:
    delinquency_ratio = st.number_input("Delinquency Ratio (%)", 0, 100, 30)
    num_open_accounts = st.number_input("Open Loan Accounts", 1, 20, 2)

loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])

# ========================= ANALYSIS BUTTON =========================
if st.button("🔍 Analyze Credit Risk"):
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

    with st.spinner("Processing request..."):
        try:
            r = requests.post(API_URL, json=payload)
            if r.status_code == 200:
                result = r.json()

                # Display ML Results
                st.markdown('<div class="section-title">Assessment Results</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class='result-card'>
                    <p><strong>Default Probability:</strong> {result['probability']:.2%}</p>
                    <p><strong>Credit Score:</strong> {result['credit_score']}</p>
                    <p><strong>Rating:</strong> {result['rating']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Display LLM advisor
                if result.get("advisor_response"):
                    st.markdown('<div class="section-title">AI Credit Advisor</div>', unsafe_allow_html=True)
                    st.markdown(f"<div class='advisor-box'>{result['advisor_response']}</div>", unsafe_allow_html=True)

                # Save session data for chatbot
                st.session_state.probability = result["probability"]
                st.session_state.credit_score = result["credit_score"]
                st.session_state.rating = result["rating"]
                st.session_state.advisor_reply = result["advisor_response"]
                st.session_state.analysis_done = True

            else:
                st.error(f"API Error: {r.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# ========================= CHATBOT =========================
if st.session_state.analysis_done:

    st.markdown("<div class='section-title'>💬 Interactive Loan Chat Assistant</div>", unsafe_allow_html=True)

    CHAT_URL = st.secrets["CHAT_URL"]
    user_query = st.text_input("Ask a follow-up question:")

    if st.button("Send Message"):
        if user_query.strip():

            payload = {
                "thread_id": st.session_state.thread_id,
                "message": user_query,
                "probability": st.session_state.probability,
                "credit_score": st.session_state.credit_score,
                "rating": st.session_state.rating,
                "advisor_reply": st.session_state.advisor_reply
            }

            r = requests.post(CHAT_URL, json=payload)

            if r.status_code == 200:
                reply = r.json()["response"]
                st.session_state.chat_history.append(("user", user_query))
                st.session_state.chat_history.append(("bot", reply))
            else:
                st.error("Chat server error.")

    for role, msg in st.session_state.chat_history:
        bubble = "chat-bubble-user" if role == "user" else "chat-bubble-bot"
        st.markdown(f"<div class='{bubble}'>{msg}</div>", unsafe_allow_html=True)
