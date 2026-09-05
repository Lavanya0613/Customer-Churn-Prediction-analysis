import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

def prepare_powerbi_dataset():
    # 1. Load base cleaned data
    df = pd.read_csv('data/processed/cleaned_telco_churn.csv')
    if 'churn_value' in df.columns:
        df['churn'] = df['churn_value']
    
    df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')
    df = df.dropna(subset=['total_charges']).copy()
    
    # 2. Re-create Segments (ML Logic)
    features = ['tenure_months', 'monthly_charges']
    df['is_month_to_month'] = (df['contract'] == 'Month-to-month').astype(int)
    df['has_tech_support'] = (df['tech_support'] == 'Yes').astype(int)
    df['has_online_security'] = (df['online_security'] == 'Yes').astype(int)
    
    cluster_features = features + ['is_month_to_month', 'has_tech_support', 'has_online_security']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[cluster_features])
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    cluster_names = {
        0: 'Uncommitted Budget',
        1: 'Premium Loyalists',
        2: 'High-Flight-Risk',
        3: 'Engaged Support Users'
    }
    df['customer_segment'] = df['cluster'].map(cluster_names)
    
    # 3. Generate Predictions for ALL Customers (for the Risk Explorer)
    try:
        pipeline = joblib.load('models/logistic_regression_pipeline.pkl')
    except:
        pipeline = joblib.load('models/xgboost_pipeline.pkl')
        
    y_prob = pipeline.predict_proba(df)[:, 1]
    df['churn_probability'] = y_prob
    
    # 4. Assign Risk Levels and Recommendations
    def assign_risk_and_action(prob):
        if prob > 0.60:
            return 'Critical', 'Immediate Intervention (Discount/Manager Call)'
        elif prob > 0.20:
            return 'High', 'Proactive Retention Campaign (Service Upgrade)'
        elif prob > 0.05:
            return 'Medium', 'Standard Engagement (Email Check-in)'
        else:
            return 'Low', 'No Action Required'
            
    risk_data = [assign_risk_and_action(p) for p in df['churn_probability']]
    df['risk_level'] = [x[0] for x in risk_data]
    df['recommended_action'] = [x[1] for x in risk_data]
    
    # Retention Priority (2x2 Matrix)
    def determine_retention_priority(row):
        is_high_value = row.get('cltv', 0) > 4500
        is_high_risk = row['churn_probability'] > 0.20
        
        if is_high_value and is_high_risk:
            return "Priority Retention"
        elif not is_high_value and is_high_risk:
            return "Standard Retention"
        elif is_high_value and not is_high_risk:
            return "Proactive Engagement"
        else:
            return "Monitor"
            
    df['retention_priority'] = df.apply(determine_retention_priority, axis=1)
    
    # 5. Top Risk Factor (Simplified rule-based extraction for Power BI display)
    def determine_top_risk_factor(row):
        if row['contract'] == 'Month-to-month' and row['churn_probability'] > 0.2:
            return "Month-to-Month Contract"
        elif row['tenure_months'] < 6 and row['churn_probability'] > 0.2:
            return "Early Lifecycle (Short Tenure)"
        elif row['tech_support'] == 'No' and row['churn_probability'] > 0.2:
            return "Lack of Tech Support"
        elif row['monthly_charges'] > 80 and row['churn_probability'] > 0.2:
            return "High Monthly Charges"
        else:
            return "Stable Profile"
            
    df['top_risk_factor'] = df.apply(determine_top_risk_factor, axis=1)
    
    # Clean up temporary columns
    df = df.drop(columns=['cluster', 'is_month_to_month', 'has_tech_support', 'has_online_security'])
    
    # 6. Save Final Dataset for Power BI
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/powerbi_dataset.csv', index=False)
    print("Dashboard data successfully exported to data/processed/powerbi_dataset.csv")

if __name__ == "__main__":
    prepare_powerbi_dataset()
