import streamlit as st
import requests
import uuid

# ----------------------------------------------------------------
# 🚀 App Setup
# ----------------------------------------------------------------

st.set_page_config(
    page_title="RiskGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

API_URL = st.secrets["API_URL"]
CHAT_URL = st.secrets["CHAT_URL"]

# ----------------------------------------------------------------
# 🎨 Enhanced Styling
# ----------------------------------------------------------------

st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Input Form Styling */
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    .section-header {
        color: #1e3c72;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Input Fields */
    .stNumberInput, .stSelectbox, .stSlider {
        margin-bottom: 1rem;
    }
    
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: #2d3748;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Results Card */
    .results-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        margin: 2rem 0;
    }
    
    .score-display {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .score-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        min-width: 200px;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .score-item h3 {
        color: white;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .score-item .value {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Advisor Box */
    .advisor-container {
        background: linear-gradient(135deg, #f6f8fb 0%, #e9ecf1 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin-top: 2rem;
    }
    
    .advisor-container h3 {
        color: #1e3c72;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .advisor-content {
        color: #2d3748;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-header {
        padding: 1rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(255,255,255,0.2);
    }
    
    .sidebar-header h2 {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
    }
    
    .sidebar-description {
        font-size: 0.85rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Chat Box */
    .chat-container {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        height: 400px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin: 0.8rem 0;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: rgba(102, 126, 234, 0.9);
        margin-left: 2rem;
        text-align: right;
    }
    
    .bot-message {
        background: rgba(255,255,255,0.95);
        margin-right: 2rem;
        color: #2d3748 !important;
    }
    
    .bot-message * {
        color: #2d3748 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat Input */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        color: #2d3748;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(45, 55, 72, 0.6);
    }
    
    /* Success Message */
    .success-banner {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(72, 187, 120, 0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 🧠 Sidebar Chatbot
# ----------------------------------------------------------------

with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h2>💬 Chat With RiskGuard AI</h2>
            <div class="sidebar-description">
                Ask questions about your loan approval, score improvement, risk factors and eligibility.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Chat container with better styling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for role, msg in st.session_state.chat_history:
            css_class = "user-message" if role == "user" else "bot-message"
            st.markdown(f'<div class="chat-message {css_class}">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 2rem; opacity: 0.7;">
                <p>👋 Welcome! Complete an analysis to start chatting.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    user_message = st.text_input(
        "Message",
        placeholder="How can I improve my credit score?",
        disabled=not st.session_state.analysis_done,
        label_visibility="collapsed",
        key="chat_input"
    )

    if st.button("Send Message", use_container_width=True, disabled=not st.session_state.analysis_done):
        if user_message and user_message.strip():
            payload = {
                "thread_id": st.session_state.thread_id,
                "message": user_message
            }
            
            try:
                with st.spinner("Thinking..."):
                    res = requests.post(CHAT_URL, json=payload, timeout=30).json()
                    reply = res.get("response", "⚠️ No response received.")

                st.session_state.chat_history.append(("user", user_message))
                st.session_state.chat_history.append(("bot", reply))
                st.rerun()

            except requests.exceptions.Timeout:
                st.error("⚠️ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"⚠️ Chat service unavailable: {str(e)}")

# ----------------------------------------------------------------
# 🏦 Main App Content
# ----------------------------------------------------------------

# Header
st.markdown("""
    <div class="main-header">
        <h1>🛡️ RiskGuard AI</h1>
        <p>Advanced Credit Risk Assessment & Financial Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)

# Input Form
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📋 Loan Application Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**👤 Personal Information**")
    age = st.number_input("Age", 18, 100, 28, help="Applicant's age")
    income = st.number_input("Annual Income (₹)", 0, 30000000, 900000, step=50000, help="Total annual income")
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])

with col2:
    st.markdown("**💰 Loan Details**")
    loan_amount = st.number_input("Loan Amount (₹)", 0, 20000000, 2500000, step=100000)
    loan_tenure_months = st.number_input("Loan Tenure (Months)", 1, 360, 36)
    loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
    loan_purpose = st.selectbox("Loan Purpose", ["Home", "Auto", "Business", "Personal", "Education"])

with col3:
    st.markdown("**📊 Credit History**")
    avg_dpd_per_delinquency = st.number_input("Avg Days Past Due", 0, 200, 10, help="Average days payment was delayed")
    delinquency_ratio = st.slider("Delinquency Ratio (%)", 0, 100, 30, help="Percentage of late payments")
    credit_utilization_ratio = st.slider("Credit Utilization (%)", 0, 100, 40, help="Percentage of credit limit used")
    num_open_accounts = st.number_input("Active Loan Accounts", 1, 10, 2)

st.markdown('</div>', unsafe_allow_html=True)

# Analyze Button
col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
with col_btn2:
    analyze_button = st.button("🔍 Analyze Credit Risk", use_container_width=True, type="primary")

# ----------------------------------------------------------------
# 🧮 Analysis Results
# ----------------------------------------------------------------

if analyze_button:
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

    try:
        with st.spinner("🔄 Analyzing your financial profile..."):
            result = requests.post(API_URL, json=payload, timeout=30).json()
        
        st.session_state.latest_result = result
        st.session_state.analysis_done = True
        
    except requests.exceptions.Timeout:
        st.error("⚠️ Request timed out. Please try again.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Analysis service unavailable: {str(e)}")
        st.stop()

# Display results if available
if st.session_state.latest_result:
    result = st.session_state.latest_result
    
    st.markdown('<div class="results-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Credit Assessment Report</div>', unsafe_allow_html=True)
    
    # Score Display
    st.markdown('<div class="score-display">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="score-item">
            <h3>Credit Score</h3>
            <div class="value">{result['credit_score']}</div>
        </div>
        <div class="score-item">
            <h3>Default Risk</h3>
            <div class="value">{result['probability']:.2%}</div>
        </div>
        <div class="score-item">
            <h3>Credit Rating</h3>
            <div class="value">{result['rating']}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Advisor Insights
    st.markdown(f"""
        <div class="advisor-container">
            <h3>🤖 AI Advisor Insights</h3>
            <div class="advisor-content">{result['advisor_response']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Success message
    if st.session_state.analysis_done:
        st.markdown("""
            <div class="success-banner">
                ✅ Analysis complete! You can now chat with the AI advisor in the sidebar for personalized guidance.
            </div>
        """, unsafe_allow_html=True)
