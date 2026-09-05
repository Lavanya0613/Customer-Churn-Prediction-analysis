import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom scikit-learn transformer to engineer features for the Telco Churn dataset.
    This ensures transformations can be applied seamlessly within a Pipeline 
    to both train and test sets without data leakage.
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # No internal state needs to be learned from the data for these specific features
        return self

    def transform(self, X):
        # Create a copy to avoid SettingWithCopyWarning
        X_eng = X.copy()
        
        # 1. Service Count (Usage/Service Adoption Feature)
        # Sum of all internet-based add-on services
        services = ['online_security', 'online_backup', 'device_protection', 
                    'tech_support', 'streaming_tv', 'streaming_movies']
        
        X_eng['service_count'] = 0
        for svc in services:
            if svc in X_eng.columns:
                X_eng['service_count'] += (X_eng[svc] == 'Yes').astype(int)
                
        # 2. Is Automatic Payment (Payment Behavior Feature)
        if 'payment_method' in X_eng.columns:
            X_eng['is_automatic_payment'] = X_eng['payment_method'].str.contains('automatic').astype(int)
            
        # 3. Recent Price Change / Spend Delta (Spending Feature)
        # Historical average spend = total_charges / tenure_months
        # If current monthly_charges > historical average, they experienced a price hike.
        if 'total_charges' in X_eng.columns and 'tenure_months' in X_eng.columns and 'monthly_charges' in X_eng.columns:
            # Handle tenure = 0 to avoid division by zero
            safe_tenure = X_eng['tenure_months'].replace(0, 1)
            historical_avg = X_eng['total_charges'] / safe_tenure
            X_eng['spend_delta'] = X_eng['monthly_charges'] - historical_avg
            
        # 4. Has Internet (Service Adoption Feature)
        if 'internet_service' in X_eng.columns:
            X_eng['has_internet'] = (X_eng['internet_service'] != 'No').astype(int)
            
        return X_eng

# Grouping definitions for pipeline architecture
RAW_NUMERICAL_FEATURES = ['tenure_months', 'monthly_charges', 'total_charges', 'cltv']
RAW_CATEGORICAL_FEATURES = ['gender', 'senior_citizen', 'partner', 'dependents', 
                            'phone_service', 'multiple_lines', 'internet_service', 
                            'online_security', 'online_backup', 'device_protection', 
                            'tech_support', 'streaming_tv', 'streaming_movies', 
                            'contract', 'paperless_billing', 'payment_method']

ENGINEERED_NUMERICAL_FEATURES = ['service_count', 'spend_delta']
ENGINEERED_CATEGORICAL_FEATURES = ['is_automatic_payment', 'has_internet']

EDA_ONLY_FEATURES = ['count', 'country', 'state', 'lat_long', 'city', 'zip_code']
LEAKAGE_FEATURES = ['churn_score', 'churn_reason', 'churn_label']
TARGET_FEATURE = ['churn_value']
