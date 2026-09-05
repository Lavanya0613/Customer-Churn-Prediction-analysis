# SHAP Explainable AI (XAI) Report

This report utilizes SHAP (SHapley Additive exPlanations) to interpret the predictive behavior of our machine learning model.

> [!WARNING]
> **Important Disclaimer on Causation**
> SHAP describes *model behavior* rather than proving real-world *causation*. It tells us mathematically how the model weighs each feature to arrive at its prediction based on historical correlations. It does not definitively prove that altering a specific feature (e.g., forcing a customer onto a different contract) will directly cause a change in their churn behavior in reality.

## Global Explainability Insights

Across the entire customer base, the model relies on several core drivers to determine risk:
1. **Contract Type (Month-to-Month vs Two Year)**: This is consistently the most powerful feature. The model heavily penalizes month-to-month contracts.
2. **Tenure**: The model assigns significantly higher risk to new customers. As tenure increases, the model drastically reduces the predicted churn probability.
3. **Monthly Charges / Fiber Optic**: High monthly charges, often associated with Fiber Optic internet, strongly push the model to predict churn.
4. **Tech Support / Online Security**: The absence of these services acts as a strong signal to the model that the customer is at risk.

## Individual Customer Explainability

By analyzing specific customers from the test set, we can translate complex model math into actionable business context.

### High-Risk Profile: Customer CUST-9
- **Churn Probability:** 99.86%
- **Risk Classification:** High

**Business Interpretation**: This customer has a very high predicted churn probability. The model's strongest contributing factors driving this risk higher typically include having a Month-to-Month contract, short tenure, and lacking technical support. The model's strongest contributing factors driving risk lower (if any) are outweighed by these risk factors.

### High-Risk Profile: Customer CUST-1099
- **Churn Probability:** 99.16%
- **Risk Classification:** High

**Business Interpretation**: This customer has a very high predicted churn probability. The model's strongest contributing factors driving this risk higher typically include having a Month-to-Month contract, short tenure, and lacking technical support. The model's strongest contributing factors driving risk lower (if any) are outweighed by these risk factors.

### Low-Risk Profile: Customer CUST-0
- **Churn Probability:** 0.03%
- **Risk Classification:** Low

**Business Interpretation**: This customer has a very low predicted churn probability. The model's strongest contributing factors keeping this risk low include having a long-term contract (One or Two Year) and long tenure. The model considers this customer highly stable and no retention action is necessary.

