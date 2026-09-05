# ML Baseline Report

## Overview
This report evaluates our initial Machine Learning baselines for the Customer Churn Prediction problem.

### Rationale for Logistic Regression Baseline
Logistic Regression is the gold standard baseline for binary classification tasks. 
- **Interpretable**: The coefficients directly indicate feature importance and direction.
- **Robust**: It rarely wildly overfits and serves as a strict floor for more complex models (like XGBoost).
- **Well-Calibrated**: It outputs genuine probabilities rather than just hard classifications, which is essential for calculating expected value or churn risk scores.

### Methodology
1. **Data Leakage Prevention**: We dropped `churn_score`, `churn_reason`, and `churn_label`.
2. **Stratified Split**: 80/20 train-test split, stratifying on `churn_value` to maintain the 26.5% churn prevalence.
3. **Strict Pipeline**: `FeatureEngineer` $\rightarrow$ `StandardScaler` (Numerical) / `OneHotEncoder` (Categorical) $\rightarrow$ `LogisticRegression`. All preprocessing was fitted strictly on `X_train`.

## Baseline Comparison

| Metric | Naive Baseline (Majority Class) | Logistic Regression |
| :--- | :--- | :--- |
| **Accuracy** | 0.735 | **0.804** |
| **Precision** | 0.000 | **0.647** |
| **Recall** | 0.000 | **0.578** |
| **F1 Score** | 0.000 | **0.610** |
| **ROC-AUC** | 0.500 | **0.849** |
| **PR-AUC** | 0.265 | **0.645** |

## Analysis
- **The Accuracy Trap**: The naive baseline achieves 73.5% accuracy simply by guessing that *no one* will ever churn. This perfectly illustrates why Accuracy is a deceptive metric for imbalanced data.
- **LR Performance**: Our Logistic Regression pipeline easily defeats the naive baseline across all meaningful metrics. An ROC-AUC of 0.849 is excellent for a first-pass untuned linear model.
- **F1 & PR-AUC**: An F1 of 0.610 and PR-AUC of 0.645 indicate that while the model is strong, there is significant room for improvement in balancing precision and recall. Advanced tree-based models (XGBoost) should be able to capture non-linear relationships to push this higher.
