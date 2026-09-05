import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.predict_model import ChurnPredictor
from src.explainability.explain_predictions import SHAPExplainer
from src.evaluation.score_customers import RecommendationEngine

class ModelService:
    def __init__(self):
        self.predictor = None
        self.explainer = None
        self.engine = None
        
    def load_models(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'logistic_regression.joblib')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
            
        self.predictor = ChurnPredictor(model_path)
        self.explainer = SHAPExplainer(self.predictor.get_pipeline())
        self.engine = RecommendationEngine()
        
    def predict_single(self, customer_data: dict) -> dict:
        df = pd.DataFrame([customer_data])
        
        # We need raw data features (excluding churn_value and customerid if they exist in a weird way)
        X = df.drop(columns=['churn_value', 'customerid'], errors='ignore')
        
        probabilities, risk_levels = self.predictor.predict_risk(X)
        explanations = self.explainer.explain_instances(X)
        
        row_data = {
            'customer_id': customer_data.get('customerid', 'UNKNOWN'),
            'churn_probability': probabilities[0],
            'risk_level': risk_levels[0],
            'top_risk_factor': explanations[0]['top_risk_factor'],
            'protective_factors': explanations[0]['top_protective_factor'],
            'contract': customer_data.get('contract'),
            'tech_support': customer_data.get('tech_support'),
            'online_security': customer_data.get('online_security'),
            'tenure_months': customer_data.get('tenure_months', 0),
            'monthly_charges': customer_data.get('monthly_charges', 0),
            'total_charges': customer_data.get('total_charges', 0)
        }
        
        recommended_action = self.engine.generate_recommendation(row_data)
        cltv = customer_data.get('cltv', 0)
        retention_priority = self.engine.get_retention_priority(cltv, row_data['risk_level'])
        
        return {
            'customer_id': row_data['customer_id'],
            'churn_probability': round(row_data['churn_probability'], 4),
            'risk_level': row_data['risk_level'],
            'top_risk_factor': row_data['top_risk_factor'],
            'protective_factors': row_data['protective_factors'],
            'recommended_action': recommended_action,
            'retention_priority': retention_priority
        }

    def predict_batch(self, customers_data: list) -> list:
        results = []
        for cust in customers_data:
            results.append(self.predict_single(cust))
        return results

model_service = ModelService()
