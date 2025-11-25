import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="RiskGuard AI: Credit Risk Modelling",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for clean, compact styling
st.markdown("""
    <style>
    .main {
        max-width: 800px;
        padding: 1rem;
        margin: 0 auto;
    }
    .block-container {
        max-width: 800px;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: 0 auto;
    }
    h1 {
        color: #2c3e50;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.3rem !important;
    }
    .subtitle {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .section-divider {
        border-top: 1px solid #e0e0e0;
        margin: 1.5rem 0 1rem 0;
    }
    .section-title {
        color: #34495e;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    .stButton>button {
        width: 100%;
        background: #3498db;
        color: white;
        font-weight: 600;
        padding: 0.6rem;
        border: none;
        border-radius: 6px;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background: #2980b9;
    }
    .calculated-metric {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #3498db;
        margin: 0.8rem 0;
    }
    .metric-label {
        color: #7f8c8d;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
    }
    .result-card {
        background: #ecf0f1;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .result-item {
        display: flex;
        justify-content: space-between;
        padding: 0.6rem 0;
        border-bottom: 1px solid #d5d8dc;
    }
    .result-item:last-child {
        border-bottom: none;
    }
    .result-label {
        color: #7f8c8d;
        font-weight: 500;
    }
    .result-value {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ RiskGuard AI")
st.markdown('<p class="subtitle">Credit Risk Assessment Platform</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle" style="color:blue; font-weight:bold;">The app could take up to <b>20 seconds</b> when using for the first time due to API cold start.</p>',
    unsafe_allow_html=True
)


# Personal & Loan Information
st.markdown('<div class="section-title">Personal & Loan Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input('Age', min_value=18, max_value=100, value=28, step=1)
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, step=100000)
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])

with col2:
    income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=50000)
    loan_tenure_months = st.number_input('Tenure (months)', min_value=0, value=36, step=1)
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])

# Calculate and display loan to income ratio
loan_to_income_ratio = loan_amount / income if income > 0 else 0
st.markdown(f"""
<div class="calculated-metric">
    <div class="metric-label">Loan to Income Ratio</div>
    <div class="metric-value">{loan_to_income_ratio:.2f}</div>
</div>
""", unsafe_allow_html=True)

# Credit Information
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Credit Information</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    avg_dpd_per_delinquency = st.number_input('Avg Days Past Due', min_value=0, value=20)
    credit_utilization_ratio = st.number_input('Credit Utilization (%)', min_value=0, max_value=100, value=30, step=1)

with col4:
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, value=30, step=1)
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, value=2, step=1)

loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

# Analysis Button
if st.button('🔍 Analyze Credit Risk'):
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
    
    with st.spinner('Analyzing...'):
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Assessment Results</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-item">
                        <span class="result-label">Default Probability</span>
                        <span class="result-value">{result['probability']:.2%}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Credit Score</span>
                        <span class="result-value">{result['credit_score']}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Credit Rating</span>
                        <span class="result-value">{result['rating']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ Analysis completed successfully")
                
            else:
                st.error(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")


