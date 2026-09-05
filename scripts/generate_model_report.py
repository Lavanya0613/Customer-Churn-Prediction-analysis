import pandas as pd
import os

def generate_report():
    df = pd.read_csv('data/processed/model_comparison.csv')
    
    report_content = """# Predictive Model Evaluation & Comparison

This report details the rigorous evaluation of multiple machine learning models to predict customer churn. To ensure robustness and prevent data leakage, all preprocessing (scaling, imputation, encoding) was performed strictly inside `scikit-learn` pipelines fitted only on the training data.

## Standard Evaluation Metrics (Threshold = 0.50)

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC | Selected? |
|-------|-----------|--------|----|---------|--------|-----------|
"""
    
    for _, row in df.iterrows():
        report_content += f"| {row['Model']} | {row['Precision']:.3f} | {row['Recall']:.3f} | {row['F1']:.3f} | {row['ROC-AUC']:.3f} | {row['PR-AUC']:.3f} | **{row['Selected?']}** |\n"
        
    report_content += """

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
"""

    os.makedirs('reports', exist_ok=True)
    with open('reports/model_comparison.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print("Report generated at reports/model_comparison.md")

if __name__ == "__main__":
    generate_report()
