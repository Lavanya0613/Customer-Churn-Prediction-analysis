import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(filepath: str) -> pd.DataFrame:
    """Loads the raw dataset."""
    logger.info(f"Loading data from {filepath}")
    if filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    elif filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")
    return df

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes column names (lowercase, snake_case)."""
    df = df.copy()
    original_cols = df.columns.tolist()
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('-', '_')
                  .str.replace('(', '')
                  .str.replace(')', ''))
    logger.info("Column names standardized.")
    return df

def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Fixes data types, particularly total_charges."""
    df = df.copy()
    if 'total_charges' in df.columns:
        # Replace empty spaces with NaN, then convert to numeric
        df['total_charges'] = pd.to_numeric(df['total_charges'].replace(' ', np.nan), errors='coerce')
    logger.info("Data types fixed.")
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handles missing values based on audit findings."""
    df = df.copy()
    
    if 'total_charges' in df.columns and 'tenure_months' in df.columns:
        # Customers with 0 tenure have missing total charges. We impute with 0.0.
        missing_total = df['total_charges'].isnull().sum()
        if missing_total > 0:
            df['total_charges'] = df.apply(
                lambda row: 0.0 if pd.isnull(row['total_charges']) and row['tenure_months'] == 0 else row['total_charges'],
                axis=1
            )
            logger.info(f"Imputed {missing_total} missing values in 'total_charges' for 0-tenure customers.")
            
    # Verify no remaining missing values in total_charges
    if df['total_charges'].isnull().sum() > 0:
        logger.warning(f"Still have {df['total_charges'].isnull().sum()} missing values in total_charges.")
        
    return df

def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows if any exist."""
    df = df.copy()
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        logger.info(f"Dropped {duplicates} duplicate rows.")
    else:
        logger.info("No duplicate rows found.")
    return df

def remove_leakage_and_redundant_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Removes target leakage, post-churn info, and zero-variance/redundant columns."""
    df = df.copy()
    
    # Target leakage and redundant targets
    leakage_cols = ['churn_score', 'churn_reason', 'churn_label']
    # Zero variance / redundant features
    redundant_cols = ['count', 'country', 'state', 'lat_long']
    
    cols_to_drop = [col for col in leakage_cols + redundant_cols if col in df.columns]
    
    df = df.drop(columns=cols_to_drop)
    logger.info(f"Dropped leakage/redundant columns: {cols_to_drop}")
    return df

def validate_data(df: pd.DataFrame):
    """Validates the dataset to ensure quality before saving."""
    logger.info("Running validation checks...")
    
    # 1. Target exists
    assert 'churn_value' in df.columns, "Validation Failed: Target column 'churn_value' is missing."
    
    # 2. No missing values in critical columns
    assert df['churn_value'].isnull().sum() == 0, "Validation Failed: Missing values in target column."
    assert df['total_charges'].isnull().sum() == 0, "Validation Failed: Missing values in total_charges."
    
    # 3. No unexpected duplicate IDs
    if 'customerid' in df.columns:
        assert df['customerid'].duplicated().sum() == 0, "Validation Failed: Duplicate customer IDs found."
        
    # 4. Numerical columns have valid types
    assert pd.api.types.is_numeric_dtype(df['total_charges']), "Validation Failed: total_charges is not numeric."
    assert pd.api.types.is_numeric_dtype(df['tenure_months']), "Validation Failed: tenure_months is not numeric."
    assert pd.api.types.is_numeric_dtype(df['monthly_charges']), "Validation Failed: monthly_charges is not numeric."
    
    logger.info("Validation passed successfully.")

def process_data(input_path: str, output_path: str):
    """Executes the full cleaning pipeline."""
    df_raw = load_data(input_path)
    
    logger.info(f"Shape before cleaning: {df_raw.shape}")
    logger.info(f"Missing values before cleaning: {df_raw.isnull().sum().sum()}")
    
    df_clean = clean_column_names(df_raw)
    df_clean = fix_data_types(df_clean)
    df_clean = handle_missing_values(df_clean)
    df_clean = handle_duplicates(df_clean)
    df_clean = remove_leakage_and_redundant_cols(df_clean)
    
    validate_data(df_clean)
    
    logger.info(f"Shape after cleaning: {df_clean.shape}")
    logger.info(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save processed data
    df_clean.to_csv(output_path, index=False)
    logger.info(f"Cleaned dataset saved to {output_path}")

if __name__ == "__main__":
    INPUT_FILE = r"C:\Users\lavanya\Desktop\my projects\Customer Churn Analysis & Prediction\data\raw\Telco_customer_churn.xlsx"
    OUTPUT_FILE = r"C:\Users\lavanya\Desktop\my projects\Customer Churn Analysis & Prediction\data\processed\cleaned_telco_churn.csv"
    process_data(INPUT_FILE, OUTPUT_FILE)
