# 🛡️ RiskGuard AI | Intelligent Credit Risk Modelling & Advisory System

## ▶️ Live App
🌍 **Streamlit App**: [https://credit-risk-model-ubh6j8cdappfztmu4tbmvz.streamlit.app/](https://credit-risk-model-ubh6j8cdappfztmu4tbmvz.streamlit.app/)  

🚀 **Overview**  
RiskGuard AI is a complete AI-powered credit risk assessment platform designed to simulate real banking decision systems.  
It combines:  
- A trained machine learning model to predict default risk  
- A credit scoring logic  
- A personalized AI loan advisor  
- A memory-powered conversational chatbot  

Users receive not only a score and risk category but also real-world style approval reasoning and improvement suggestions.

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 📊 **Credit Risk Prediction Model** | Uses machine learning (XGBoost) to estimate probability of default |
| 🧠 **Credit Scoring Engine** | Converts model output into a realistic credit score and rating |
| 🏦 **Approval-style Decision Logic** | Approve, decline, or conditional feedback |
| 🤖 **AI Financial Advisor** | Generates human-like reasoning and personalized feedback |
| 💬 **Interactive Chatbot** | Lets users ask follow-up questions and receive contextual answers |
| 🧷 **Thread Memory** | Chatbot remembers past answers and user state using LangGraph memory |
| 🎨 **Modern UI** | Responsive, professional UI built in Streamlit (automatically enhanced using AI styling) |

## 📦 Dataset
- **Size**: 50,000+ borrower records  
- **Features**: Loan behavior, credit bureau metadata, repayment history  
- **Target**: "default" (binary classification)

## 🧹 Data Preprocessing
- Missing value handling  
- Outlier treatment (Winsorization)  
- One-hot encoding for categorical fields  
- Numerical scaling using Min-Max Normalization  
- Feature filtering using: Information Value (IV), Variance Inflation Factor (VIF), Manual domain checks

## 📊 Model Performance

| Metric | Result |
|--------|--------|
| **AUC** | 0.98 |
| **Gini Coefficient** | 0.96 |
| **KS Statistic** | 48% (strong discrimination in early deciles) |

Additional evaluation: ROC Curve, Confusion Matrix, Decile Lift Chart

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Uvicorn |
| **ML** | Pandas, NumPy, Scikit-learn, XGBoost |
| **LLM** | Groq Llama-3.1 via LangChain + LangGraph |
| **Frontend** | Streamlit |
| **Deployment** | Railway + Streamlit Cloud |
| **Secrets Management** | .env locally and secrets.toml in Streamlit |

## 🧩 Architecture
User → Streamlit UI
→ FastAPI (Model + LLM logic)
→ (XGBoost + Scoring + Advisor Prompt)
→ Chatbot (LangGraph memory)
→ Response → UI


## 🧠 AI Components

1. **Advisor Model Prompt**  
   Generates a short and precise approval response based on model output.  
   Example structure: Greeting → Decision → Risk score explanation → Actionable tips → CTA: continue conversation with AI chatbot

2. **Memory Chatbot**  
   Provides follow-up answers like:  
   - "Why was my loan rejected?"  
   - "How can I increase my approval chances?"  
   - "What should I fix first?"  
   Memory is persistent per thread_id.

## 🎨 UI Notes
The initial version was a simple functional UI. Once validated, the frontend was improved using AI assistance to match a professional fintech product experience.

## 🚀 Quick Start
1. Clone repo: `git clone <your-repo-url>`  
2. Install: `pip install -r requirements.txt`  
3. Run: `streamlit run app.py`  
4. Access: `http://localhost:8501`

