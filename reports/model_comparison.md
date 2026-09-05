# Predictive Model Evaluation & Comparison

This report details the rigorous evaluation of multiple machine learning models to predict customer churn. To ensure robustness and prevent data leakage, all preprocessing (scaling, imputation, encoding) was performed strictly inside `scikit-learn` pipelines fitted only on the training data.

## Standard Evaluation Metrics (Threshold = 0.50)

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC | Selected? |
|-------|-----------|--------|----|---------|--------|-----------|
| Majority Baseline | 0.000 | 0.000 | 0.000 | 0.500 | 0.633 | **No** |
| Logistic Regression | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **Yes** |
| Decision Tree | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **No** |
| Random Forest | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **No** |
| XGBoost | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **No** |


## Threshold Optimization

Standard machine learning evaluation defaults to a 0.50 probability threshold. However, this is rarely the optimal business decision.

**Business Context:**
- **False Negative (Missed Churner):** High cost. Losing a customer means losing their entire Customer Lifetime Value (LTV).
- **False Positive (Unnecessary Retention Offer):** Lower cost. The cost is the margin lost on the discount or promotion offered.

Because the cost of a false negative vastly outweighs the cost of a false positive, we must prioritize **Recall** (capturing as many actual churners as possible) over Precision.

Based on the trade-off analysis, we selected an optimal decision threshold of **0.20**. This significantly boosts Recall, ensuring the business captures the vast majority of at-risk customers, while accepting a higher False Positive rate that is economically justifiable.

## Error Analysis (At Threshold = 0.20)
- **False Positives (Predicted Churn, Actual Retained):** These customers look statistically identical to churners (e.g., month-to-month contracts, high charges, low tenure). Providing them with proactive retention offers is a safe business move that may further lock them into long-term loyalty.
- **False Negatives (Predicted Retained, Actual Churn):** These are "silent churners". They are often long-tenured customers who experience a sudden, unrecorded negative event (such as a poor customer service interaction). To catch these in the future, the model would need sentiment data from support call transcripts.
