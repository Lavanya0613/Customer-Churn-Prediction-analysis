import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.predict_model import ChurnPredictor
from src.explainability.explain_predictions import SHAPExplainer

class RecommendationEngine:
    def __init__(self):
        pass
        
    def generate_recommendation(self, row):
        """
        Interpretable business rules for recommendations.
        These are actionable suggestions based on customer state, NOT guaranteed causal interventions.
        """
        if row.get('risk_level') == "Low Risk":
            return "Monitor; No immediate intervention needed"
            
        risk_factor = str(row.get('top_risk_factor')).lower()
        
        # Rule 1: High risk + Month-to-Month contract
        if row.get('contract') == 'Month-to-month':
            return "Offer annual-contract incentive/discount"
            
        # Rule 2: High risk + Fiber Optic / High Charges (Price sensitivity)
        if 'fiber optic' in risk_factor or 'total_charges' in risk_factor or 'monthly_charges' in risk_factor:
            return "Review pricing; Consider personalized discount or downgrade option"
            
        # Rule 3: High risk + Support activity (simulated by lack of tech support / security)
        if row.get('tech_support') == 'No' or row.get('online_security') == 'No':
            return "Prioritize customer support check-in; offer free tech review"
            
        # Rule 4: High risk + low engagement (short tenure)
        if 'tenure' in risk_factor and row.get('tenure_months', 0) < 12:
            return "Deploy re-engagement campaign; improve onboarding experience"
            
        # Default
        return "Assign to Customer Success representative for manual review"

    def get_retention_priority(self, cltv, risk_level):
        """
        Calculates 2x2 matrix category based on CLTV and Risk Level.
        """
        is_high_value = cltv > 4500
        is_high_risk = risk_level in ["High Risk", "Critical Risk", "High", "Critical"]
        
        if is_high_value and is_high_risk:
            return "Priority Retention"
        elif not is_high_value and is_high_risk:
            return "Standard Retention"
        elif is_high_value and not is_high_risk:
            return "Proactive Engagement"
        else:
            return "Monitor"

def score_batch():
    model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'logistic_regression.joblib')
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'cleaned_telco_churn.csv')
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'customer_churn_predictions.csv')
    
    print("Loading data and models...")
    df = pd.read_csv(data_path)
    X = df.drop(columns=['churn_value', 'customerid'], errors='ignore')
    
    predictor = ChurnPredictor(model_path)
    explainer = SHAPExplainer(predictor.get_pipeline())
    
    print("Scoring customers...")
    probabilities, risk_levels = predictor.predict_risk(X)
    
    print("Calculating SHAP explanations...")
    explanations = explainer.explain_instances(X)
    
    print("Generating recommendations...")
    engine = RecommendationEngine()
    
    # Combine results
    results = []
    for i in range(len(df)):
        cust_id = df.loc[i, 'customerid'] if 'customerid' in df.columns else f"CUST_{i}"
        
        row_data = {
            'customer_id': cust_id,
            'churn_probability': probabilities[i],
            'risk_level': risk_levels[i],
            'top_risk_factor': explanations[i]['top_risk_factor'],
            'protective_factors': explanations[i]['top_protective_factor'],
            # We need original contract, tech_support etc. for business rules
            'contract': df.loc[i, 'contract'] if 'contract' in df.columns else None,
            'tech_support': df.loc[i, 'tech_support'] if 'tech_support' in df.columns else None,
            'online_security': df.loc[i, 'online_security'] if 'online_security' in df.columns else None,
            'tenure_months': df.loc[i, 'tenure_months'] if 'tenure_months' in df.columns else 0,
        }
        
        # Apply business rules
        row_data['recommended_action'] = engine.generate_recommendation(row_data)
        
        # Clean up columns for output
        out_row = {
            'customer_id': row_data['customer_id'],
            'churn_probability': round(row_data['churn_probability'], 4),
            'risk_level': row_data['risk_level'],
            'top_risk_factor': row_data['top_risk_factor'],
            'protective_factors': row_data['protective_factors'],
            'recommended_action': row_data['recommended_action']
        }
        results.append(out_row)
        
    out_df = pd.DataFrame(results)
    out_df.to_csv(output_path, index=False)
    print(f"Successfully scored {len(out_df)} customers and saved to {output_path}")

if __name__ == "__main__":
    score_batch()
