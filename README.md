# RiskGuard AI: Credit Risk Modelling 🚀

🔗 **Live Streamlit App**: [https://credit-risk-model-ubh6j8cdappfztmu4tbmvz.streamlit.app/)  

---

## 🧠 Project Overview

**RiskGuard AI** is an end-to-end machine learning system that predicts the likelihood of a customer defaulting on a loan. Built with financial institutions in mind, this credit risk modelling solution processes historical loan and bureau data to generate accurate, interpretable risk scores.

The application is deployed with a scalable backend API and an interactive frontend for risk analysts to assess creditworthiness in real-time.

---

## 🎯 Objective

To develop a robust and interpretable credit risk prediction model that:
- Accurately classifies the likelihood of default
- Scales well in real-world production environments
- Provides decile-wise insights and model metrics
- Integrates seamlessly into MLOps pipelines

---

## 📦 Dataset

- **Size**: 50,000 records  
- **Features**: Customer loan and bureau attributes  
- **Target Variable**: `default` (1 = Default, 0 = No Default)

---

## 🧹 Data Preprocessing

- Invalid categorical values replaced with statistical mode
- Feature selection using:
  - **Information Value (IV)**
  - **Variance Inflation Factor (VIF)**
  - **Domain knowledge**
- Numerical scaling using Min-Max normalization
- Missing value imputation

---

## 📊 Model Evaluation

| Metric                  | Target   | Achieved                           |
|-------------------------|----------|------------------------------------|
| AUC (Area Under Curve)  | > 85%    | ✅ Achieved                         |
| Gini Coefficient        | > 85     | ✅ Achieved                         |
| KS Statistic            | > 40     | ✅ Achieved (High KS in early deciles) |

Other evaluations:
- Classification Report
- Decile-wise Performance
- Confusion Matrix
- ROC Curves

---

## 🛠️ Tech Stack

**Languages & Frameworks**:
- Python, FastAPI, Streamlit

**Libraries**:
- Pandas, NumPy, Scikit-learn, XGBoost, Matplotlib, Seaborn

**MLOps & Deployment**:
- Docker
- AWS EC2 (Ubuntu)
- Streamlit Cloud
- dotenv & TOML-based secrets management

---

## 🔧 Backend API (FastAPI)

A FastAPI server was built to handle model inference requests. It separates logic for young and older users internally, using the appropriate pre-trained model.

### 🔐 Security

- Uses `.env` locally via `python-dotenv`
- Uses `secrets.toml` on Streamlit Cloud
- Dockerized for container-based deployment

---

## 🖥️ Frontend (Streamlit)

The frontend was built using **Streamlit** to offer an intuitive UI for credit risk evaluation.

### Features:
- Responsive inputs for key credit variables
- Real-time risk prediction via FastAPI
- Displays:
  - Default probability
  - Credit score
  - Risk rating

### Deployment:
- **Local**: via `streamlit run main.py`
- **Cloud**: Hosted on [Streamlit Cloud](https://credit-risk-model-zgqk3gy549secuhsiccbo7.streamlit.app/)
- Backend API integrated using `st.secrets` for secure variable handling

---

## 🐳 Docker & AWS Deployment

- Docker image created for FastAPI backend
- Pushed to DockerHub
- Deployed on **AWS EC2 (Ubuntu)**
- Port 8000 exposed for API access
- Uvicorn used as ASGI server

---
![Screenshot 2025-06-29 132552](https://github.com/user-attachments/assets/35f28216-2595-400e-9d85-e0806ddb28ae)
