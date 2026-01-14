# 🛡️ RiskGuard AI

### Intelligent Credit Risk Modeling & AI Advisory System

---

## 🔗 Live Application

🌍 **Frontend (GitHub Pages)**
👉 https://junaidariie.github.io/Credit-Risk-Model/

🚀 **Backend API (FastAPI on Hugging Face Spaces)**
👉 Deployed with real-time inference & streaming support

---
## High-Level Architecture Diagram (Riskguard  AI)

                        ┌────────────────────────────┐
                        │        Frontend UI         │
                        │ (Form + Results + Chat UI) │
                        └──────────────┬─────────────┘
                                       │
                                       ▼
                        ┌────────────────────────────┐
                        │           FastAPI          │
                        │        app.py (API)        │
                        └──────────────┬─────────────┘
                                       │
             ┌─────────────────────────┼─────────────────────────┐
             │                         │                         │
             ▼                         ▼                         ▼
    ┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
    │ Credit Risk      │    │ Insight Generator    │    │ Loan Chat Assistant  │
    │ Prediction API   │    │ (One-time bot)       │    │ (Conversational bot) │
    │ (ML Model)       │    └──────────┬───────────┘    └──────────┬───────────┘
    └─────────┬────────┘               │                           │
              │                        ▼                           ▼
              │              ┌──────────────────────┐   ┌──────────────────────┐
              │              │  Prompt + LLM Logic   │  │  Chat Orchestrator   │
              │              │  (advisor logic)      │  │  (memory + context)  │
              │              └──────────┬───────────┘   └──────────┬───────────┘
              │                         │                          │
              │                         ▼                          ▼
    ┌──────────────────┐     ┌──────────────────────┐   ┌──────────────────────┐
    │ Feature Pipeline │     │  TTS Engine          │   │  TTS Engine          │
    │ (preprocess, FE) │     │ (Text → Speech)      │   │ (Text → Speech)      │
    └──────────────────┘     └──────────────────────┘   └──────────────────────┘
    

## 🚀 Project Overview

**RiskGuard AI** is an end-to-end **AI-powered credit risk assessment and advisory system** designed to simulate how modern financial institutions evaluate loan applications.

The platform integrates:

* Machine learning–based credit risk prediction
* Intelligent scoring and decision logic
* An AI-powered conversational advisor
* Speech-to-text (STT) and text-to-speech (TTS) interaction
* Real-time streaming responses

The system is designed to feel like a **real-world fintech decision engine**, combining analytics, explainability, and conversational intelligence.

---

## 🎯 Key Features

| Feature                         | Description                                                     |
| ------------------------------- | --------------------------------------------------------------- |
| 📊 **Credit Risk Prediction**   | Machine learning model predicts default probability             |
| 🧠 **Credit Scoring Engine**    | Converts predictions into interpretable risk scores             |
| 🏦 **Decision Logic**           | Produces approval, conditional, or rejection decisions          |
| 🤖 **AI Financial Advisor**     | Provides human-like explanations and recommendations            |
| 💬 **Conversational Chatbot**   | Users can ask follow-up questions in natural language           |
| 🧷 **Context Memory**           | Maintains conversation context using LangGraph                  |
| 🔊 **Text-to-Speech (TTS)**     | Converts AI responses into natural speech                       |
| 🎙️ **Speech-to-Text (STT)**    | Allows voice-based user interaction                             |
| 🌐 **Live Web Search (Tavily)** | Enhances chatbot responses with up-to-date information          |
| ⚡ **Streaming Responses**       | Real-time token streaming from the backend                      |
| 🎨 **Modern UI**                | Clean, responsive interface built using AI-assisted HTML/CSS/JS |

---

## 📊 Dataset Overview

* **Size:** 50,000+ customer records
* **Target Variable:** `default` (binary classification)
* **Feature Categories:**

  * Credit utilization & repayment behavior
  * Income & employment details
  * Loan characteristics
  * Demographic attributes

---

## 🧹 Data Preprocessing

* Missing value handling
* Outlier treatment (Winsorization)
* Categorical encoding
* Min–Max normalization
* Feature selection using:

  * Information Value (IV)
  * Variance Inflation Factor (VIF)
  * Domain-driven filtering

---

## 📈 Model Performance

| Metric               | Score |
| -------------------- | ----- |
| **AUC**              | 0.98  |
| **Gini Coefficient** | 0.96  |
| **KS Statistic**     | 48%   |

Additional evaluation includes:

* ROC Curve
* Confusion Matrix
* Decile Lift Analysis

---

## 🧠 AI Architecture

### 1️⃣ Credit Risk Model

A supervised machine learning model trained on structured financial data to estimate default probability with high interpretability.

---

### 2️⃣ AI Advisor (LLM-powered)

Generates human-like explanations based on:

* Model outputs
* Risk category
* Credit behavior

It provides:

* Decision justification
* Improvement suggestions
* Context-aware guidance

---

### 3️⃣ Conversational Memory

Implemented using **LangGraph**, enabling:

* Persistent conversational context
* Follow-up reasoning
* Stateful interactions

---

### 4️⃣ Speech & Interaction Layer

* **Text-to-Speech (TTS):** Converts AI responses into natural voice
* **Speech-to-Text (STT):** Enables voice-based user input
* **Streaming responses:** Real-time conversational experience

---

## 🧩 System Architecture

```
User
  ↓
Frontend (HTML / CSS / JS)
  ↓
FastAPI Backend
  ├── Credit Risk Model
  ├── Scoring Logic
  ├── AI Advisor (LLM)
  ├── Tavily Search (Live Knowledge)
  ├── LangGraph Memory
  ├── TTS / STT Engine
  ↓
Streaming Response → UI
```

---

## 🛠️ Tech Stack

| Layer          | Technology                                 |
| -------------- | ------------------------------------------ |
| **Frontend**   | HTML, CSS, JavaScript (AI-assisted design) |
| **Backend**    | FastAPI                                    |
| **ML**         | Pandas, NumPy, Scikit-learn                |
| **LLM**        | Groq (LLaMA 3.1) / gpt-4.1-nano            |
| **Memory**     | LangGraph                                  |
| **Search**     | Tavily API                                 |
| **Speech**     | Edge TTS + Whisper (STT)                   |
| **Deployment** | Hugging Face Spaces, GitHub Pages          |
| **Secrets**    | `.env` & platform secrets                  |

---

## 🎯 Real-World Applications

* Credit approval simulation
* Fintech decision support systems
* AI-driven financial assistants
* Risk analysis training tools
* Explainable AI demonstrations

---

## 🚀 Future Enhancements

* Emotion-aware voice synthesis
* Multilingual support
* Real-time speech streaming
* User profile personalization
* Explainable AI dashboards (SHAP)

---

## 👤 Author

**Junaid**
AI / Machine Learning Engineer
Focused on building real-world, production-grade AI systems.

---

## ⭐ Final Note

RiskGuard AI demonstrates how **machine learning, conversational AI, and real-time systems** can be combined to build intelligent, explainable financial applications used in modern fintech ecosystems.
