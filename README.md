## 🛡️ RiskGuard AI

### Production-Grade Credit Risk Engine + AI Advisory System

---

## 🔗 Live Application

🌍 **Frontend (GitHub Pages)**
👉 [https://junaidariie.github.io/Credit-Risk-Model/](https://junaidariie.github.io/Credit-Risk-Model/)

🚀 **Backend API (FastAPI on Hugging Face Spaces)**
👉 Deployed with real-time inference, streaming responses, and AI advisory

---

## 🎥 Demo Video

📺 **Watch the full project demo on YouTube**
👉 [YouTube Demo Link](YOUR_YOUTUBE_LINK_HERE)

---

## 🧭 High-Level Architecture (RiskGuard AI)

```
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
```

---

## 🚀 Project Overview

**RiskGuard AI** is an end-to-end, production-style **credit risk decisioning platform** that simulates how modern banks and fintech companies evaluate loan applications.

It combines:

* **Machine Learning risk modeling**
* **Scorecard-based credit scoring logic**
* **Config-driven data pipelines**
* **AI-powered advisory (LLM)**
* **Conversational chatbot with memory**
* **Speech-to-Text (STT) & Text-to-Speech (TTS)**
* **Streaming real-time responses**

This project is intentionally built to resemble **real enterprise ML architecture**, not notebook-style demos.

---

## 🎯 Core Capabilities

| Capability                    | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| 📊 **Credit Risk Prediction** | Logistic Regression model predicts probability of default |
| 🧮 **Scorecard Engine**       | Converts probability into credit score (300–900 scale)    |
| 🏷️ **Risk Rating**           | Buckets customers into Poor / Average / Good / Excellent  |
| 🤖 **AI Advisor (LLM)**       | Explains decisions and gives improvement guidance         |
| 💬 **Conversational Chatbot** | Follow-up questions with memory & context                 |
| 🔊 **Text-to-Speech (TTS)**   | Converts insights into natural voice                      |
| 🎙️ **Speech-to-Text (STT)**  | Voice input support                                       |
| ⚡ **Streaming Responses**     | Token-level streaming from backend                        |
| 🧠 **LangGraph Memory**       | Stateful conversations                                    |
| 🌐 **Tavily Web Search**      | Live knowledge augmentation                               |

---

## 🗂️ Production-Grade Project Structure

```
credit-risk-cmplt/
│
├── .github/
│   └── workflows/
│       └── ci.yaml                 # GitHub Actions CI pipeline
│
├── config/
│   └── config.yaml                # Central config (paths, params, model settings)
│
├── data/
│   └── raw/                        # Raw dataset (CSV)
│
├── src/
│   ├── ingestion.py                # Data loading
│   ├── preprocessing.py            # Cleaning + feature engineering
│   ├── train.py                    # Training pipeline + versioning
│   ├── evaluate.py                 # Model evaluation (AUC, metrics)
│   └── utils.py                    # Config loader, versioning utilities
│
├── inference/
│   └── predictor.py                # Inference logic (scorecard + model)
│
├── models/                         # Versioned models, scalers, columns
│   ├── credit_model_*.pkl
│   ├── scaler_*.pkl
│   └── columns_*.pkl
│
├── tests/                          # End-to-end & unit tests
│   ├── test_ingestion.py
│   ├── test_preprocessing.py
│   ├── test_training.py
│   ├── test_evaluation.py
│   └── test_full_pipeline.py
│
├── advisor_bot.py                  # One-time AI insight generator
├── chatbot_advisor.py              # Conversational AI assistant
├── utility.py                      # STT & TTS utilities
├── app.py                          # FastAPI application
├── index.html                      # Frontend UI
├── Dockerfile                      # HF Spaces deployment
├── requirements.txt
└── README.md
```

---

## 📊 Dataset Overview

* **Size:** 50,000+ records
* **Target:** `default` (0 = good, 1 = default)
* **Feature Domains:**

  * Credit utilization
  * Delinquency behavior
  * Income & employment
  * Loan characteristics
  * Demographics

---

## 🧹 Data Preprocessing & Feature Engineering

Implemented in `src/preprocessing.py`:

* Missing value handling
* Business rule filtering
* Derived features:

  * `loan_to_income`
  * `delinquency_ratio`
  * `avg_dpd_per_delinquency`
* One-hot encoding
* Column alignment for inference

---

## 🏗️ Training Pipeline (Config-Driven)

Implemented in `src/train.py`:

* Config loaded from `config/config.yaml`
* Steps:

  1. Ingestion
  2. Preprocessing
  3. Encoding
  4. Scaling (MinMaxScaler)
  5. Class imbalance handling (SMOTETomek)
  6. Logistic Regression training
  7. **Automatic versioning** of:

     * model
     * scaler
     * columns

Each training run creates timestamped artifacts.

---

## 📈 Model Performance

| Metric   | Value |
| -------- | ----- |
| **AUC**  | ~0.99 |
| **Gini** | ~0.98 |
| **KS**   | ~85%  |

Evaluated via `src/evaluate.py`.

---

## 🧠 Credit Scorecard Logic

Implemented in `inference/predictor.py`:

```python
score = 300 + (1 - PD) * 600
```

| Score Range | Rating    |
| ----------- | --------- |
| 300–500     | Poor      |
| 500–650     | Average   |
| 650–750     | Good      |
| 750–900     | Excellent |

This mimics **real banking scorecard systems**.

---

## 🤖 AI Advisory System

### 1️⃣ One-Time Advisor

* Generates explanation after prediction
* Uses LLM + risk context

### 2️⃣ Conversational Assistant

* LangGraph-based memory
* Stateful conversation
* Follow-up reasoning

---

## 🔊 Voice & Interaction Layer

* **STT (Speech → Text)** via Whisper
* **TTS (Text → Speech)** via Edge TTS
* Integrated directly into FastAPI

---

## 🔄 CI/CD Pipeline

This project includes a fully automated **GitHub Actions CI pipeline** (`.github/workflows/ci.yaml`).  
All tests run automatically on every push — ensuring code quality and reliability.

✅ **CI Status: All tests passing**

![CI Pipeline](assets/ci-pipeline.png)

---

## ⚙️ Testing (Enterprise Style)

All core components are **individually and end-to-end tested**:

```bash
python tests/test_ingestion.py
python tests/test_preprocessing.py
python tests/test_training.py
python tests/test_evaluation.py
python tests/test_full_pipeline.py
```

---

## 🛠️ Tech Stack

| Layer      | Tech                              |
| ---------- | --------------------------------- |
| Frontend   | HTML, CSS, JS                     |
| Backend    | FastAPI                           |
| ML         | Pandas, NumPy, Scikit-learn       |
| LLM        | Groq (LLaMA 3.1), OpenAI          |
| Memory     | LangGraph                         |
| Search     | Tavily API                        |
| Speech     | Whisper (STT), Edge TTS           |
| Deployment | Hugging Face Spaces, GitHub Pages |

---

## 🎯 Real-World Relevance

This project closely resembles:

* Bank credit engines
* Fintech underwriting systems
* Risk analytics platforms
* AI-powered financial advisors

It is designed to demonstrate **production thinking, not just ML modeling**.

---

## 👤 Author

**Junaid**
AI / Machine Learning Engineer
Focused on building production-grade, real-world AI systems.

---

## ⭐ Final Note

RiskGuard AI is intentionally engineered to show:

* Proper data pipelines
* Config-driven architecture
* Versioned models
* Scorecard logic
* AI integration
* Testing discipline
