# Data Cleaning Report

## Overview
This document summarizes the data cleaning transformations applied to the raw IBM Telco Customer Churn dataset. The raw file `data/raw/Telco_customer_churn.xlsx` was left strictly unmodified. The processing logic is implemented in reusable Python functions within `src/data/clean_data.py`.

## Summary Statistics

| Metric | Before Cleaning | After Cleaning |
| :--- | :--- | :--- |
| **Rows** | 7,043 | 7,043 |
| **Columns** | 33 | 26 |
| **Missing Values** | 5,174 | 0 |
| **Duplicate Rows** | 0 | 0 |

## Transformations Performed

1. **Standardized Column Names**: 
   - Converted to lowercase.
   - Replaced spaces and hyphens with underscores.
   - Stripped trailing/leading whitespace and parentheses.
2. **Fixed Data Types**: 
   - Evaluated `total_charges`. Encountered 11 string spaces `" "` instead of numerical missing indicators. 
   - Successfully converted `total_charges` to float.
3. **Handled Missing Values**: 
   - Found 11 missing values in `total_charges` resulting from customers with `tenure_months == 0`.
   - **Action**: Imputed missing `total_charges` with `$0.00` since these represent brand new customers who have not yet been billed.
4. **Validation Checks Implemented**:
   - Asserts target column `churn_value` exists.
   - Asserts zero missing values in `churn_value` and `total_charges`.
   - Asserts zero duplicated `customerid` rows.
   - Asserts valid numerical data types for critical features.

## Excluded Columns & Rationale

| Column Dropped | Rationale |
| :--- | :--- |
| `churn_score` | **Target Leakage**. IBM's proprietary prediction metric. |
| `churn_reason` | **Target Leakage**. Only available post-churn. (Responsible for 5,174 missing values). |
| `churn_label` | **Redundant**. Represents the exact same information as `churn_value` (Yes/No vs 1/0). |
| `count` | **Zero Variance**. All rows contain the value 1. |
| `country` | **Zero Variance**. All rows contain "United States". |
| `state` | **Zero Variance**. All rows contain "California". |
| `lat_long` | **Redundant**. Data is already fully represented by individual `latitude` and `longitude` columns. |

**Note on Outliers**: No automated outlier removal was performed to preserve legitimate minority patterns (e.g. high-value customers). High-cardinality categorical variables (City, Zip Code) were retained in the dataset, but should be dropped or encoded during the ML feature selection phase.
