# 🚀 Customer Churn Intelligence & Retention Analytics Platform

![Project Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge)

A full-stack, machine-learning-powered platform designed to identify high-risk telecommunications customers and provide actionable retention strategies. This project goes beyond basic classification by integrating business rules, Customer Lifetime Value (CLTV), and SHAP explainability into a beautiful, real-time Glassmorphism dashboard.

---

## 🌟 Key Features

* **Real-time Scoring API**: A robust FastAPI backend serving a fine-tuned Logistic Regression model.
* **Premium Dashboard UI**: A custom-built, responsive React frontend featuring a dark space theme with glowing Glassmorphism components.
* **Live Prediction Engine**: Input customer parameters via the UI and instantly receive a churn probability and an actionable retention strategy.
* **XAI (Explainable AI)**: Uses SHAP (SHapley Additive exPlanations) to explain exactly *why* a customer is flagged as high-risk (e.g., month-to-month contract, lack of tech support).
* **Automated Retention Prioritization**: Categorizes at-risk customers into a 2x2 matrix (Priority Retention, Standard Retention, Proactive Engagement, Monitor) based on their risk level and CLTV.
* **Full Containerization**: Entire stack (Frontend, Backend, PostgreSQL DB) runs seamlessly via Docker Compose.

---

## 🏗️ Architecture

The application is deployed via a modern single-node IaaS architecture using Docker Compose.

1. **Frontend**: React 18 + Vite, Recharts for data visualization, Vanilla CSS (Glassmorphism design system).
2. **Backend**: FastAPI, Scikit-Learn (Pipelines, Logistic Regression), SHAP, Uvicorn.
3. **Database**: PostgreSQL (persists live model predictions).
4. **Data Science Pipeline**: Jupyter Notebooks for EDA, K-Means Segmentation, and Model Training (`/notebooks`).

---

## 🚀 Quick Start (Docker)

Ensure you have [Docker](https://www.docker.com/) and Docker Compose installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lavanya0613/Customer-Churn-Prediction-analysis.git
   cd "Customer-Churn-Prediction-analysis"
   ```

2. **Build and launch the containers:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   * **Dashboard UI**: [http://localhost](http://localhost)
   * **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 Business Analytics & Segments

Before modeling, the data underwent rigorous exploratory analysis and K-Means segmentation.
Customers fall into interpretable business segments based on tenure, service adoption, and charges:
* **High-Value Loyalists**: Long tenure, high CLTV, low risk.
* **New & At-Risk**: Short tenure, high monthly charges, high risk.
* **Price-Sensitive Basic**: DSL/No Internet, low monthly charges.

## 🧠 Machine Learning Performance

The production model is a **Logistic Regression** classifier optimized for **Recall** (to ensure we capture as many churning customers as possible) while maintaining a healthy F1-score. 
All preprocessing (scaling, encoding, imputation) is strictly encapsulated within Scikit-Learn Pipelines to prevent data leakage.

* **Optimal Threshold**: `0.20`
* **Baseline Accuracy**: Evaluated against a majority-class baseline.
* **Explainability**: SHAP global and local feature importance integrated directly into the API payload.

---

## 📂 Project Structure

```text
├── api/                   # FastAPI application & endpoints
├── data/                  # Raw and processed datasets
├── frontend/              # React UI (Vite)
├── models/                # Serialized ML models (joblib)
├── notebooks/             # Data Science workflow & research
├── scripts/               # Automation & data pipeline scripts
├── src/                   # Core Python ML modules
├── docker-compose.yml     # Infrastructure orchestration
└── README.md              # Project documentation
```

---

*Designed and engineered by Lavanya.*
