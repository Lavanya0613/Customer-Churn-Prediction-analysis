import pandas as pd
import numpy as np
import json
import shap
import sys
import os

# Add src to path to import FeatureEngineer
sys.path.append(os.path.abspath('.'))
from src.features.build_features import FeatureEngineer

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix, roc_auc_score, average_precision_score
from sklearn.dummy import DummyClassifier

def load_data():
    df = pd.read_csv('data/processed/cleaned_telco_churn.csv')
    
    # Target variable setup
    # If the column is churn_value, map to churn
    if 'churn_value' in df.columns:
        df['churn'] = df['churn_value']
    
    fe = FeatureEngineer()
    df = fe.transform(df)
    
    X = df.drop(columns=['customer_id', 'churn', 'churn_value', 'churn_score', 'churn_reason', 'churn_label', 'count', 'country', 'state', 'lat_long', 'city', 'zip_code'], errors='ignore')
    y = df['churn']
    
    numeric_features = ['tenure_months', 'monthly_charges', 'total_charges', 'service_count', 'spend_delta']
    categorical_features = ['contract', 'internet_service', 'payment_method', 'gender', 'senior_citizen']
    
    # Keep only relevant columns for simplicity
    X = X[numeric_features + categorical_features]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
        ])
    
    return df, X, y, preprocessor, numeric_features, categorical_features

def get_kde_data(series, bins=30):
    hist, edges = np.histogram(series.dropna(), bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    return [{"x": float(c), "y": float(h)} for c, h in zip(centers, hist)]

def main():
    print("Loading data...")
    df, X, y, preprocessor, numeric_features, categorical_features = load_data()
    
    analytics = {}
    
    # 1. Executive Overview & EDA
    print("Generating EDA stats...")
    analytics['kpis'] = {
        'total_customers': int(len(df)),
        'churn_rate': float(df['churn'].mean()),
        'avg_mrr': float(df['monthly_charges'].mean())
    }
    
    analytics['churn_by_contract'] = df.groupby('contract')['churn'].mean().reset_index().rename(columns={'churn': 'rate'}).to_dict('records')
    analytics['churn_by_internet'] = df.groupby('internet_service')['churn'].mean().reset_index().rename(columns={'churn': 'rate'}).to_dict('records')
    
    analytics['tenure_dist_churned'] = get_kde_data(df[df['churn'] == 1]['tenure_months'])
    analytics['tenure_dist_retained'] = get_kde_data(df[df['churn'] == 0]['tenure_months'])
    
    analytics['charges_dist_churned'] = get_kde_data(df[df['churn'] == 1]['monthly_charges'])
    analytics['charges_dist_retained'] = get_kde_data(df[df['churn'] == 0]['monthly_charges'])
    
    # Correlation (numeric only)
    corr_cols = ['tenure_months', 'monthly_charges', 'total_charges', 'service_count', 'spend_delta', 'churn']
    corr = df[corr_cols].corr()
    corr_data = []
    for col1 in corr.columns:
        for col2 in corr.columns:
            corr_data.append({"x": col1, "y": col2, "value": float(corr.loc[col1, col2])})
    analytics['correlation'] = corr_data
    
    # 2. Customer Segmentation
    print("Generating Segmentation stats...")
    if 'segment' not in df.columns:
        def segment_customer(row):
            if row['contract'] == 'Month-to-month' and row['tenure_months'] < 12:
                return 'High-Flight-Risk'
            elif row['contract'] == 'Month-to-month' and row['tenure_months'] >= 12:
                return 'Uncommitted'
            elif row['contract'] != 'Month-to-month' and row['monthly_charges'] > 70:
                return 'Premium'
            else:
                return 'Budget'
        df['segment'] = df.apply(segment_customer, axis=1)
        
    scatter_sample = df.sample(min(500, len(df)), random_state=42)
    analytics['segment_scatter'] = scatter_sample[['tenure_months', 'monthly_charges', 'segment', 'churn']].to_dict('records')
    
    segment_stats = []
    for seg, group in df.groupby('segment'):
        q1 = group['total_charges'].quantile(0.25)
        median = group['total_charges'].median()
        q3 = group['total_charges'].quantile(0.75)
        min_val = group['total_charges'].min()
        max_val = group['total_charges'].max()
        segment_stats.append({
            "segment": seg, "min": float(min_val), "q1": float(q1), "median": float(median), "q3": float(q3), "max": float(max_val)
        })
    analytics['segment_box'] = segment_stats
    
    # 3. ML Benchmarking
    print("Benchmarking Models...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    models = {
        'Baseline': DummyClassifier(strategy='most_frequent'),
        'Logistic Regression': LogisticRegression(max_iter=1000, class_weight='balanced'),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, class_weight='balanced', random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=50, max_depth=5, class_weight='balanced', random_state=42),
        'XGBoost': XGBClassifier(eval_metric='logloss', random_state=42, scale_pos_weight=(len(y_train)-sum(y_train))/sum(y_train))
    }
    
    roc_data = {}
    pr_data = {}
    metrics = []
    
    for name, model in models.items():
        print(f"Training {name}...")
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        pipeline.fit(X_train, y_train)
        
        if hasattr(pipeline.named_steps['classifier'], "predict_proba"):
            y_probs = pipeline.predict_proba(X_test)[:, 1]
        else:
            y_probs = np.zeros(len(y_test))
            
        fpr, tpr, _ = roc_curve(y_test, y_probs)
        precision, recall, _ = precision_recall_curve(y_test, y_probs)
        
        auc_roc = roc_auc_score(y_test, y_probs) if name != 'Baseline' else 0.5
        auc_pr = average_precision_score(y_test, y_probs) if name != 'Baseline' else float(y_train.mean())
        
        idx = np.linspace(0, len(fpr)-1, min(30, len(fpr)), dtype=int)
        roc_data[name] = [{"x": float(fpr[i]), "y": float(tpr[i])} for i in idx]
        
        idx = np.linspace(0, len(precision)-1, min(30, len(precision)), dtype=int)
        pr_data[name] = [{"x": float(recall[i]), "y": float(precision[i])} for i in idx]
        
        metrics.append({
            "name": name,
            "roc_auc": float(auc_roc),
            "pr_auc": float(auc_pr)
        })
        
        if name == 'Logistic Regression':
            cm = confusion_matrix(y_test, y_probs >= 0.20)
            analytics['confusion_matrix'] = [
                {"actual": "Retained", "predicted": "Retained", "value": int(cm[0,0])},
                {"actual": "Retained", "predicted": "Churned", "value": int(cm[0,1])},
                {"actual": "Churned", "predicted": "Retained", "value": int(cm[1,0])},
                {"actual": "Churned", "predicted": "Churned", "value": int(cm[1,1])}
            ]
            
            thresholds = np.linspace(0, 1, 30)
            tradeoff = []
            for t in thresholds:
                cm_t = confusion_matrix(y_test, y_probs >= t)
                if cm_t.shape == (2,2):
                    tp = cm_t[1,1]
                    fp = cm_t[0,1]
                    fn = cm_t[1,0]
                    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
                    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
                    
                    net_value = (tp * 100) - (fp * 20)
                    tradeoff.append({
                        "threshold": float(t),
                        "precision": float(prec),
                        "recall": float(rec),
                        "net_value": float(net_value)
                    })
            analytics['threshold_tradeoff'] = tradeoff
            
            print("Calculating SHAP...")
            X_train_transformed = pipeline.named_steps['preprocessor'].transform(X_train)
            feature_names = numeric_features + list(pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features))
            
            explainer = shap.LinearExplainer(pipeline.named_steps['classifier'], X_train_transformed)
            sample_idx = np.random.choice(X_train_transformed.shape[0], 200, replace=False)
            shap_values = explainer.shap_values(X_train_transformed[sample_idx])
            
            mean_abs_shap = np.abs(shap_values).mean(axis=0)
            shap_importance = sorted([{"feature": feature_names[i], "importance": float(mean_abs_shap[i])} for i in range(len(feature_names))], key=lambda x: x['importance'], reverse=True)
            analytics['shap_importance'] = shap_importance[:10]

    analytics['roc_curves'] = roc_data
    analytics['pr_curves'] = pr_data
    analytics['model_metrics'] = metrics

    print("Saving analytics JSON...")
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', models['Logistic Regression'])])
    pipeline.fit(X_train, y_train)
    y_probs = pipeline.predict_proba(X_test)[:, 1]
    
    analytics['risk_distribution'] = get_kde_data(pd.Series(y_probs), bins=20)
    
    with open('data/processed/analytics_dashboard.json', 'w') as f:
        json.dump(analytics, f)
        
    print("Done! Analytics saved to data/processed/analytics_dashboard.json")

if __name__ == "__main__":
    main()
