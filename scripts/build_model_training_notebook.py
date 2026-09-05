import nbformat as nbf
import os

def create_training_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Model Training
**Customer Churn Intelligence & Retention Analytics Platform**

This notebook covers rigorous model training, strictly preventing data leakage by using scikit-learn pipelines. We will train and compare:
1. Majority-Class Baseline
2. Logistic Regression
3. Decision Tree
4. Random Forest
5. XGBoost"""))

    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import joblib
import os
import sys

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

import warnings
warnings.filterwarnings('ignore')"""))

    cells.append(nbf.v4.new_markdown_cell("""## Data Loading and Splitting"""))
    cells.append(nbf.v4.new_code_cell("""df = pd.read_csv('../data/processed/cleaned_telco_churn.csv')
if 'churn_value' in df.columns:
    df['churn'] = df['churn_value']

df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')
df = df.dropna(subset=['total_charges']).copy()

# Features and Target
drop_cols = ['customerid', 'churn', 'churn_value', 'churn_label', 'churn_reason', 'cltv', 'city', 'zip_code', 'latitude', 'longitude']
X = df.drop(columns=[col for col in drop_cols if col in df.columns])
y = df['churn']

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")"""))

    cells.append(nbf.v4.new_markdown_cell("""## Sklearn Preprocessing Pipeline
We must fit scalers and encoders ONLY on the training data to prevent leakage."""))
    cells.append(nbf.v4.new_code_cell("""num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols)
    ])"""))

    cells.append(nbf.v4.new_markdown_cell("""## Model Training Dictionary"""))
    cells.append(nbf.v4.new_code_cell("""models = {
    'Majority Baseline': DummyClassifier(strategy='most_frequent'),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=7, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42, eval_metric='logloss')
}

trained_models = {}
predictions = {}
probabilities = {}

print("Training models...")
for name, model in models.items():
    print(f"Training {name}...")
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', model)])
    
    pipeline.fit(X_train, y_train)
    trained_models[name] = pipeline
    
    # Store predictions for evaluation notebook
    predictions[name] = pipeline.predict(X_test)
    if hasattr(pipeline.named_steps['classifier'], "predict_proba"):
        probabilities[name] = pipeline.predict_proba(X_test)[:, 1]
    else:
        # For Dummy Classifier (most frequent)
        probabilities[name] = pipeline.predict_proba(X_test)[:, 1]

print("Training complete.")"""))

    cells.append(nbf.v4.new_markdown_cell("""## Export Models and Predictions"""))
    cells.append(nbf.v4.new_code_cell("""os.makedirs('../models', exist_ok=True)

for name, pipeline in trained_models.items():
    file_name = name.replace(" ", "_").lower()
    joblib.dump(pipeline, f'../models/{file_name}_pipeline.pkl')

# Save predictions for eval
eval_data = pd.DataFrame({'y_test': y_test})
for name in models.keys():
    eval_data[f'{name}_pred'] = predictions[name]
    eval_data[f'{name}_prob'] = probabilities[name]

eval_data.to_csv('../data/processed/model_predictions.csv', index=False)
X_test.to_csv('../data/processed/X_test.csv', index=False)
print("Artifacts saved successfully.")"""))

    nb['cells'] = cells
    os.makedirs('notebooks', exist_ok=True)
    with open('notebooks/08_model_training.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Generated notebooks/08_model_training.ipynb")

if __name__ == "__main__":
    create_training_notebook()
