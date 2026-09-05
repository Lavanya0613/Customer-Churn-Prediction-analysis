# Final Model Evaluation & Threshold Recommendation

## Overview
This report finalizes our machine learning architecture by evaluating our best candidate model (**Logistic Regression**) on the isolated test set. Crucially, we reject the default statistical threshold (0.5) in favor of a business-optimized threshold that minimizes the financial bleed caused by churn.

## Initial Performance (Default Threshold = 0.5)
When tested on the unseen test dataset at the default probability threshold of 0.5, the Logistic Regression model achieved:
- **ROC-AUC**: 0.849
- **PR-AUC**: 0.645
- **Accuracy**: 0.804
- **Precision**: 0.647
- **Recall**: 0.578
- **F1 Score**: 0.610

**Error Analysis at 0.5:**
The model is fairly precise, meaning when it flags someone as a churner, it is usually correct (65% of the time). However, its **Recall of 57.8% is unacceptable for a retention business**. This means we are completely missing 42.2% of all customers who are about to churn. 

## Business Sensitivity Analysis
In churn prediction, missing a churner (False Negative) is significantly more expensive than accidentally giving a discount to a loyal customer (False Positive). 

To find the mathematically optimal threshold, we simulated the following hypothetical costs:
- **Cost of a False Negative**: $100 (Lost customer lifetime value/revenue)
- **Cost of a False Positive**: $20 (Cost of a retention marketing campaign wasted on someone who wasn't leaving)
- **Cost of a True Positive**: $20 (Cost of the retention campaign to successfully save the customer)

We evaluated classification thresholds from 0.1 to 0.8. 

| Threshold | Precision | Recall | F1 Score | Customers Flagged | Total Business Cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0.1 | 0.414 | 0.947 | 0.576 | 856 | $19,120 |
| **0.2** | **0.481** | **0.861** | **0.617** | **669** | **$18,580** |
| 0.3 | 0.531 | 0.746 | 0.621 | 525 | $20,000 |
| 0.4 | 0.579 | 0.668 | 0.620 | 432 | $21,040 |
| 0.5 | 0.647 | 0.578 | 0.610 | 334 | $22,480 |
| 0.8 | 0.800 | 0.043 | 0.081 | 20 | $36,200 |

## Final Recommendation

- **Final Model**: Logistic Regression Pipeline (Custom Feature Engineer $\rightarrow$ Standard Scaler $\rightarrow$ OHE $\rightarrow$ LR)
- **Final Threshold**: **0.20**
- **Final Metrics (at 0.20)**: Precision = 0.481, Recall = **0.861**, F1 = 0.617

**Rationale**:
By drastically lowering the threshold to `0.20`, we cast a wider net. Our precision drops (we will contact many people who weren't actually going to churn), but our **Recall skyrockets from 57% to 86%**. We correctly identify and intervene with the vast majority of our at-risk customers.

Under our cost assumptions, remaining at the default 0.5 threshold costs the business **$22,480** per test cohort. By lowering the threshold to 0.2, the total business cost drops to **$18,580**—an immediate 17.3% reduction in financial loss. Mathematical accuracy is secondary; minimizing business cost is the primary objective.
