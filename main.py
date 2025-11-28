import streamlit as st
import requests
import uuid
from datetime import datetime

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
if "show_info" not in st.session_state:
    st.session_state.show_info = False

# ========================= ENHANCED UI STYLING =========================
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 2rem 0;
}

/* Header Styling */
.header-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    text-align: center;
}

.header-title {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.header-subtitle {
    color: #e0e7ff;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

/* Section Cards */
.section-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    margin-bottom: 1.5rem;
    border-left: 4px solid #667eea;
}

.section-title {
    color: #1e293b;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Info Box */
.info-box {
    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #f39c12;
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: transform 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    margin: 0.5rem 0;
}

.metric-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

/* Result Cards */
.result-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 2rem;
    border-radius: 16px;
    color: white;
    box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
    margin: 1.5rem 0;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
}

.result-item {
    background: rgba(255,255,255,0.2);
    padding: 1.5rem;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.result-item-label {
    font-size: 0.9rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.result-item-value {
    font-size: 1.8rem;
    font-weight: 700;
}

/* Advisor Box */
.advisor-box {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin-top: 1.5rem;
    border-left: 4px solid #3498db;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.advisor-box h4 {
    color: #2c3e50;
    margin-top: 0;
}

/* Chat Bubbles */
.chat-container {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px auto;
    max-width: 70%;
    text-align: right;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    animation: slideInRight 0.3s ease-out;
}

.chat-bubble-bot {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px auto 8px 0;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    animation: slideInLeft 0.3s ease-out;
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.8rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

/* Progress Bar */
.progress-container {
    margin: 1rem 0;
}

/* Input Fields */
.stNumberInput>div>div>input,
.stSelectbox>div>div>select,
.stTextInput>div>div>input {
    border-radius: 8px;
    border: 2px solid #e9ecef;
    padding: 0.5rem;
    transition: border-color 0.3s ease;
}

.stNumberInput>div>div>input:focus,
.stSelectbox>div>div>select:focus,
.stTextInput>div>div>input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Alert Banner */
.alert-banner {
    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #f39c12;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Scrollbar Styling */
.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}
</style>
""", unsafe_allow_html=True)

# ========================= HEADER =========================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🛡️ RiskGuard AI</h1>
    <p class="header-subtitle">Advanced AI-Powered Credit Risk Assessment Platform</p>
</div>
""", unsafe_allow_html=True)

# Alert Banner
st.markdown("""
<div class="alert-banner">
    ⚠️ <strong>Note:</strong> First request may take up to 20 seconds (API cold start).
</div>
""", unsafe_allow_html=True)

# Info Toggle
if st.button("ℹ️ How It Works"):
    st.session_state.show_info = not st.session_state.show_info

if st.session_state.show_info:
    st.markdown("""
    <div class="info-box">
        <h4>📊 About RiskGuard AI</h4>
        <p><strong>What we analyze:</strong></p>
        <ul>
            <li>Personal financial profile and credit history</li>
            <li>Loan-to-income ratio and debt burden</li>
            <li>Payment patterns and delinquency records</li>
            <li>Credit utilization and account management</li>
        </ul>
        <p><strong>Our AI provides:</strong></p>
        <ul>
            <li>Default probability predictions</li>
            <li>Credit score assessment</li>
            <li>Risk rating classification</li>
            <li>Personalized recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ========================= INPUT FORM =========================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Personal & Loan Information</div>', unsafe_allow_html=True)
    
    age = st.number_input("Age", 18, 100, 28, help="Applicant's age in years")
    income = st.number_input("Annual Income (₹)", 0, 50000000, 1200000, step=50000, help="Total annual income")
    loan_amount = st.number_input("Loan Amount (₹)", 0, 50000000, 2500000, step=100000, help="Requested loan amount")
    loan_tenure_months = st.number_input("Loan Tenure (months)", 0, 480, 36, help="Loan repayment period")
    
    loan_purpose = st.selectbox("Loan Purpose", ["Education", "Home", "Auto", "Personal"])
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])
    loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display Loan-to-Income Ratio
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Loan-to-Income Ratio</div>
        <div class="metric-value">{loan_to_income_ratio:.2f}x</div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💳 Credit Profile</div>', unsafe_allow_html=True)
    
    avg_dpd_per_delinquency = st.number_input("Average Days Past Due", 0, 200, 20, help="Average days past due per delinquency")
    delinquency_ratio = st.number_input("Delinquency Ratio (%)", 0, 100, 30, help="Percentage of delinquent accounts")
    credit_utilization_ratio = st.number_input("Credit Utilization (%)", 0, 100, 30, help="Percentage of available credit used")
    num_open_accounts = st.number_input("Open Loan Accounts", 1, 20, 2, help="Number of currently active loan accounts")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================= ANALYSIS BUTTON =========================
st.markdown("<br>", unsafe_allow_html=True)

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

    with st.spinner("🤖 Analyzing your credit profile..."):
        try:
            r = requests.post(API_URL, json=payload, timeout=30)
            if r.status_code == 200:
                result = r.json()

                # Display Results
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-top:0; color:white;">📊 Assessment Results</h3>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="result-grid">
                    <div class="result-item">
                        <div class="result-item-label">Default Probability</div>
                        <div class="result-item-value">{result['probability']:.2%}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-item-label">Credit Score</div>
                        <div class="result-item-value">{result['credit_score']}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-item-label">Risk Rating</div>
                        <div class="result-item-value">{result['rating']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Display AI Advisor
                if result.get("advisor_response"):
                    st.markdown(f"""
                    <div class="advisor-box">
                        <h4>🤖 AI Credit Advisor Insights</h4>
                        <p>{result['advisor_response']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Save to session
                st.session_state.probability = result["probability"]
                st.session_state.credit_score = result["credit_score"]
                st.session_state.rating = result["rating"]
                st.session_state.advisor_reply = result["advisor_response"]
                st.session_state.analysis_done = True
                
                st.success("✅ Analysis complete! You can now chat with our AI assistant below.")

            else:
                st.error(f"❌ API Error: {r.status_code} - {r.text}")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")

# ========================= CHATBOT =========================
if st.session_state.analysis_done:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Interactive Loan Chat Assistant</div>', unsafe_allow_html=True)

    # Display Chat History
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for role, msg in st.session_state.chat_history:
            bubble = "chat-bubble-user" if role == "user" else "chat-bubble-bot"
            prefix = "You: " if role == "user" else "🤖 Assistant: "
            st.markdown(f"<div class='{bubble}'><strong>{prefix}</strong>{msg}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input
    user_query = st.text_input("Ask a question about your credit assessment:", placeholder="e.g., How can I improve my credit score?")

    col_send, col_clear = st.columns([3, 1])
    
    with col_send:
        send_button = st.button("📤 Send Message", use_container_width=True)
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

    if send_button and user_query.strip():
        CHAT_URL = st.secrets["CHAT_URL"]
        
        payload = {
            "thread_id": st.session_state.thread_id,
            "message": user_query,
            "probability": st.session_state.probability,
            "credit_score": st.session_state.credit_score,
            "rating": st.session_state.rating,
            "advisor_reply": st.session_state.advisor_reply
        }

        with st.spinner("🤖 Thinking..."):
            try:
                r = requests.post(CHAT_URL, json=payload, timeout=30)
                if r.status_code == 200:
                    reply = r.json()["response"]
                    st.session_state.chat_history.append(("user", user_query))
                    st.session_state.chat_history.append(("bot", reply))
                    st.rerun()
                else:
                    st.error(f"❌ Chat server error: {r.status_code}")
            except Exception as e:
                st.error(f"❌ Chat failed: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
    <p>🛡️ RiskGuard AI © 2025 | Powered by Advanced Machine Learning</p>
    <p style='font-size: 0.8rem;'>For demonstration purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
