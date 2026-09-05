# Dataset Audit Report: IBM Telco Customer Churn

## 1. Overview & Data Types
The dataset consists of 7,043 customer records and 33 columns.
- **Categorical (24)**: Represented as object/string types. Notably, `Total Charges` is initially read as a string due to blank spaces masking missing values.
- **Numerical (9)**: Comprising `Count`, `Zip Code`, `Latitude`, `Longitude`, `Tenure Months`, `Monthly Charges`, `Churn Value`, `Churn Score`, and `CLTV`.
- **Date Fields (0)**: There are no explicit datetime fields (e.g., subscription start dates), so time-based splitting is not possible.

## 2. Missingness Patterns
- **`Total Charges`**: 11 missing values. In the raw file, these are represented as blank spaces `" "`. They exactly align with the 11 customers who have a `Tenure Months` of `0` (brand new customers who haven't paid a total bill yet).
- **`Churn Reason`**: 5,174 missing values. This perfectly correlates with the customers who did not churn (5,174 `No` values in `Churn Value`).

## 3. Duplicates & Identifiers
- **Duplicate Records**: 0
- **Duplicate IDs (`CustomerID`)**: 0. Every row represents a unique customer.

## 4. Cardinality & Variance
- **Zero Variance**: `Count` (always 1), `Country` (always "United States"), `State` (always "California"). These provide no predictive value.
- **High Cardinality**: `City` (1,129 unique values) and `Zip Code` (1,652 unique values). These pose an overfitting risk for ML models if used directly.

## 5. Numerical Ranges & Outliers
- **Tenure Months**: [0, 72] (Mean: 32.4)
- **Monthly Charges**: [$18.25, $118.75] (Mean: $64.76)
- **Total Charges**: [$18.80, $8,684.80] (Mean: $2,283.30)
- **CLTV**: [2003, 6500] (Mean: 4400)
- **Outliers**: No statistically significant outliers were detected using the standard 1.5 * IQR method across numerical features.

## 6. Suspicious & Impossible Values
- **Tenure = 0**: There are 11 customers with 0 tenure. As a result, they have blank `Total Charges`. This is not impossible (they just signed up), but requires imputation (e.g., setting to $0.00).

## 7. Target Distribution & Imbalance
- **Target**: `Churn Value` (1 = Churn, 0 = Retained)
- **Retained (0)**: 5,174 (73.46%)
- **Churned (1)**: 1,869 (26.54%)
- **Class Imbalance**: Moderate (Ratio of ~2.77:1). We should consider class weighting, SMOTE, or optimizing for F1/PR-AUC rather than raw accuracy.

## 8. Correlation & Redundancy
- **Redundant Variables**: 
  - `Lat Long` is a string concatenation of `Latitude` and `Longitude`.
  - `Churn Label` (Yes/No) is identical to `Churn Value` (1/0).
- **High Correlation**: 
  - `Tenure Months` and `Total Charges` are highly positively correlated (Pearson $r \approx 0.83$). This is expected since Total = Tenure * Monthly.
  - `Latitude` and `Longitude` are highly negatively correlated ($r \approx -0.88$) due to the geographic shape of California.

## 9. Leakage & Post-Churn Variables
- **`Churn Reason`**: Only collected *after* a customer churns. Using this to predict churn is 100% target leakage.
- **`Churn Score`**: A proprietary score provided by IBM. According to dataset meta-knowledge, this score predicts the likelihood of churn. If we include it as a feature, we are essentially ensembling our model with IBM's black-box model, masking our own model's ability to learn from raw features.

---

## Data Dictionary & Classification

| column_name | data_type | description | missing_percentage | unique_count | role | ML_usage | notes |
|---|---|---|---|---|---|---|---|
| CustomerID | object | Unique alphanumeric customer ID | 0% | 7043 | Identifier | Exclude | Do not use for ML. |
| Count | int64 | Constant value 1 | 0% | 1 | EDA-only | Exclude | Zero variance. |
| Country | object | Customer Country | 0% | 1 | EDA-only | Exclude | Zero variance. |
| State | object | Customer State | 0% | 1 | EDA-only | Exclude | Zero variance. |
| City | object | Customer City | 0% | 1129 | Categorical | Exclude (initially) | High cardinality; risk of overfitting. Use Lat/Lon instead. |
| Zip Code | int64 | Customer Zip Code | 0% | 1652 | Categorical | Exclude (initially) | High cardinality. |
| Lat Long | object | Concatenated Latitude and Longitude | 0% | 1652 | EDA-only | Exclude | Redundant. |
| Latitude | float64 | Geographic Latitude | 0% | 1652 | Numerical | Include | Geographic feature. |
| Longitude | float64 | Geographic Longitude | 0% | 1651 | Numerical | Include | Geographic feature. |
| Gender | object | Customer gender (Male/Female) | 0% | 2 | Categorical | Include | Demographic feature. |
| Senior Citizen | object | Is customer a senior? (Yes/No) | 0% | 2 | Categorical | Include | Demographic feature. |
| Partner | object | Has a partner? (Yes/No) | 0% | 2 | Categorical | Include | Demographic feature. |
| Dependents | object | Has dependents? (Yes/No) | 0% | 2 | Categorical | Include | Demographic feature. |
| Tenure Months | int64 | Months staying with the company | 0% | 73 | Numerical | Include | Strong historical predictor. |
| Phone Service | object | Has phone service? (Yes/No) | 0% | 2 | Categorical | Include | Service feature. |
| Multiple Lines | object | Has multiple lines? (Yes/No/No phone) | 0% | 3 | Categorical | Include | Service feature. |
| Internet Service | object | Internet type (DSL/Fiber/No) | 0% | 3 | Categorical | Include | Service feature. |
| Online Security | object | Has online security? | 0% | 3 | Categorical | Include | Service feature. |
| Online Backup | object | Has online backup? | 0% | 3 | Categorical | Include | Service feature. |
| Device Protection | object | Has device protection? | 0% | 3 | Categorical | Include | Service feature. |
| Tech Support | object | Has tech support? | 0% | 3 | Categorical | Include | Service feature. |
| Streaming TV | object | Has streaming TV? | 0% | 3 | Categorical | Include | Service feature. |
| Streaming Movies | object | Has streaming movies? | 0% | 3 | Categorical | Include | Service feature. |
| Contract | object | Contract term (Month-to-month/One year/Two year) | 0% | 3 | Categorical | Include | Usually the strongest predictor of churn. |
| Paperless Billing | object | Uses paperless billing? (Yes/No) | 0% | 2 | Categorical | Include | Billing feature. |
| Payment Method | object | How customer pays bill | 0% | 4 | Categorical | Include | Billing feature. |
| Monthly Charges | float64 | Current monthly charge | 0% | 1585 | Numerical | Include | Financial feature. |
| Total Charges | float64 | Total charges incurred | 0.15% (11 rows) | 6530 | Numerical | Include | Requires imputation (fill 11 blanks with 0). |
| Churn Label | object | Target: Yes/No | 0% | 2 | Target | Exclude | Redundant with Churn Value. |
| Churn Value | int64 | Target: 1/0 | 0% | 2 | Target | Target | Use as primary prediction target. |
| Churn Score | int64 | IBM predicted churn score (5-100) | 0% | 85 | Leakage Risk | Exclude | Target leakage. A pre-calculated prediction from IBM. |
| CLTV | int64 | Customer Lifetime Value | 0% | 3438 | Numerical | Include | Acceptable to use if known historically. |
| Churn Reason | object | Specific reason for churning | 73.4% | 20 | Leakage Risk | Dashboard-only | 100% Target Leakage. Only known post-churn. |
