---

# 🛡️ RiskGuard AI

### Intelligent Credit Risk Modeling & AI-Driven Financial Advisory System

---

## ▶️ Live Application

🌍 **Streamlit App**
🔗 [https://junaidariie.github.io/Credit-Risk-Model/](https://junaidariie.github.io/Credit-Risk-Model/)

---

## 🚀 Overview

**RiskGuard AI** is an end-to-end **AI-powered credit risk assessment platform** designed to simulate how real-world financial institutions evaluate borrower risk and provide advisory insights.

The system goes beyond traditional prediction by combining:

* Machine Learning–based risk modeling
* Credit scoring logic inspired by real banking workflows
* An AI-powered financial advisor
* A conversational chatbot with contextual memory

Users receive **transparent risk scores**, **approval-style decisions**, and **actionable improvement recommendations**, closely mimicking real fintech decision engines.

---

## 🎯 Key Features

| Feature                             | Description                                                            |
| ----------------------------------- | ---------------------------------------------------------------------- |
| 📊 **Credit Risk Prediction Model** | Logistic Regression model estimating probability of default            |
| 🧠 **Credit Scoring Engine**        | Converts model outputs into realistic credit scores & risk bands       |
| 🏦 **Approval Decision Logic**      | Simulates bank-style approval, conditional approval, or rejection      |
| 🤖 **AI Financial Advisor**         | Generates human-like explanations and improvement strategies           |
| 💬 **Interactive Chatbot**          | Enables follow-up financial questions with contextual memory           |
| 🧷 **Thread Memory (LangGraph)**    | Maintains conversational continuity per user session                   |
| 🎨 **Modern UI**                    | Clean, responsive Streamlit interface enhanced with AI-assisted design |

---

## 📦 Dataset

* **Records:** 50,000+ borrower profiles
* **Features Include:**

  * Demographics
  * Credit utilization
  * Loan behavior
  * Repayment history
  * Bureau-level indicators
* **Target Variable:** `default` (binary classification)

---

## 🧹 Data Preprocessing

* Missing value handling
* Outlier treatment (Winsorization)
* One-hot encoding for categorical features
* Min–Max normalization
* Feature selection using:

  * Information Value (IV)
  * Variance Inflation Factor (VIF)
  * Domain-driven filtering

---

## 📊 Model Performance

| Metric               | Value                              |
| -------------------- | ---------------------------------- |
| **AUC**              | 0.98                               |
| **Gini Coefficient** | 0.96                               |
| **KS Statistic**     | 48% (strong early-risk separation) |

Additional evaluation:

* ROC Curve
* Confusion Matrix
* Decile Lift Analysis

---

## 🧠 AI System Architecture

```
User
 ↓
Streamlit UI
 ↓
FastAPI Backend
 ├── Credit Risk Model
 ├── Credit Scoring Logic
 ├── Advisory Prompt Engine
 └── LangGraph Chat Memory
 ↓
AI Response → UI
```

---

## 🧠 AI Components Explained

### 1️⃣ Advisor Model

Generates concise, decision-focused responses using structured reasoning:

**Flow:**
Greeting → Decision → Risk Explanation → Improvement Tips → Follow-up CTA

---

### 2️⃣ Conversational Memory Bot

Supports natural follow-ups such as:

* “Why was my loan rejected?”
* “How can I improve my approval chances?”
* “What should I focus on first?”

Memory persists per session using **LangGraph**.

---

## 🛠️ Tech Stack

| Layer                  | Technology                                 |
| ---------------------- | ------------------------------------------ |
| **Backend**            | FastAPI, Uvicorn                           |
| **Machine Learning**   | Pandas, NumPy, Scikit-learn                |
| **LLM**                | Groq (LLaMA-3.1) via LangChain + LangGraph |
| **Frontend**           | Streamlit                                  |
| **Deployment**         | Railway + Streamlit Cloud                  |
| **Secrets Management** | `.env` (local), `secrets.toml` (cloud)     |

---

## 🎨 UI & UX Notes

* Initial UI was functional-first
* Later enhanced using **AI-assisted design principles**
* Focused on clarity, responsiveness, and real fintech aesthetics
* Built to resemble internal banking tools rather than demos

---

## 📌 Why This Project Matters

This project demonstrates:

* Real-world **credit risk modeling**
* **End-to-end AI system design**
* Strong understanding of **financial decision pipelines**
* Integration of **ML + LLMs + APIs + UI**
* Production-style thinking and scalability

It closely mirrors how modern fintech and lending platforms operate internally.

---

## ✅ Future Enhancements (Planned)

* Multi-model ensemble (XGBoost + Logistic blend)
* User-level historical risk tracking
* Explainable AI (SHAP integration)
* Voice-based interaction (STT + TTS)
* Multi-language support

---

## 📬 Feedback & Collaboration

If you’re interested in collaboration, feedback, or discussion around AI in finance — feel free to connect.

---

