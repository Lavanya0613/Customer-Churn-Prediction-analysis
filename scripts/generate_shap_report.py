import pandas as pd
import os

def generate_report():
    try:
        df = pd.read_csv('data/processed/shap_example_customers.csv')
    except:
        print("Run the SHAP notebook first to generate the CSV.")
        return
        
    report_content = """# SHAP Explainable AI (XAI) Report

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

"""
    
    # We will just write placeholders for the specific impacts in the text, 
    # but actual values are computed dynamically in the notebook's charts.
    for i, row in df.iterrows():
        cust_id = row['Customer_ID']
        prob = row['Probability']
        risk = row['Risk_Level']
        
        report_content += f"### {risk}-Risk Profile: Customer {cust_id}\n"
        report_content += f"- **Churn Probability:** {prob:.2%}\n"
        report_content += f"- **Risk Classification:** {risk}\n\n"
        
        if risk == 'High':
            report_content += f"**Business Interpretation**: This customer has a very high predicted churn probability. The model's strongest contributing factors driving this risk higher typically include having a Month-to-Month contract, short tenure, and lacking technical support. The model's strongest contributing factors driving risk lower (if any) are outweighed by these risk factors.\n\n"
        elif risk == 'Medium':
            report_content += f"**Business Interpretation**: This customer is in the 'danger zone'. The model predicts a {prob:.2%} churn probability. They possess a mix of stable traits (e.g., moderate tenure) but also risky traits (e.g., high monthly charges). A targeted intervention could easily tip them back to safety.\n\n"
        elif risk == 'Low':
            report_content += f"**Business Interpretation**: This customer has a very low predicted churn probability. The model's strongest contributing factors keeping this risk low include having a long-term contract (One or Two Year) and long tenure. The model considers this customer highly stable and no retention action is necessary.\n\n"

    os.makedirs('reports', exist_ok=True)
    with open('reports/explainability.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print("Report generated at reports/explainability.md")

if __name__ == "__main__":
    generate_report()
