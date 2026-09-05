# Power BI Dashboard Implementation Guide
**Customer Churn Intelligence & Retention Analytics Platform**

This guide provides precise, step-by-step instructions for constructing the 6-page Business Intelligence dashboard using `data/processed/powerbi_dataset.csv`. 

**Pre-requisite:** Import `powerbi_dataset.csv` into Power BI. Ensure `monthly_charges`, `total_charges`, `tenure_months`, and `churn_probability` are typed as Decimals/Whole Numbers.

---

## PAGE 1 — EXECUTIVE OVERVIEW

### KPIs (Card Visuals)
1. **Total Customers**: `Count(customerid)`
2. **Churned Customers**: `Calculate(Count(customerid), churn == 1)`
3. **Churn Rate**: `Divide(Churned Customers, Total Customers)` (Format as %)
4. **High-Risk Customers**: `Calculate(Count(customerid), risk_level IN {"High", "Critical"})`
5. **Avg Monthly Charges**: `Average(monthly_charges)`
6. **Avg Tenure**: `Average(tenure_months)`
7. **Revenue at Risk**: `Calculate(Sum(monthly_charges), risk_level IN {"High", "Critical"})`

### Visuals
- **Customer Churn Overview (Donut Chart)**: Legend: `churn`, Values: `Count(customerid)`
- **Churn by Contract (Clustered Bar Chart)**: Axis: `contract`, Values: `Churn Rate`
- **Churn by Tenure (Line Chart)**: Axis: `tenure_months` (binned into 12-month groups), Values: `Churn Rate`
- **Customer Segment Distribution (Treemap)**: Category: `customer_segment`, Values: `Count(customerid)`

### Slicers
- `contract`, `payment_method`, `internet_service`, `customer_segment`, `risk_level`

---

## PAGE 2 — CHURN DRIVERS

### Visuals
- **Churn Rate by Payment Method (Column Chart)**: Axis: `payment_method`, Values: `Churn Rate`
- **Churn Rate by Service Type (Column Chart)**: Axis: `internet_service`, Values: `Churn Rate`
- **Monthly Charges vs Churn (Box and Whisker / Violin)**: Axis: `churn`, Values: `monthly_charges`
- **Support Activity vs Churn (100% Stacked Bar)**: Axis: `tech_support`, Legend: `churn`, Values: `Count(customerid)`

### Ranked "Observed Churn Associations" (Text/Table)
Create a table visual highlighting the highest churn rates across variables (e.g., Month-to-Month: 42%, Fiber Optic: 41%, No Tech Support: 41%). 
> **Note to Analyst**: Add a text box stating: *"These factors are heavily associated with churn mathematically, but are observational and do not imply direct causation."*

---

## PAGE 3 — CUSTOMER SEGMENTS

### Segment Risk Matrix (Scatter Plot)
- **X-Axis**: `Average(tenure_months)`
- **Y-Axis**: `Churn Rate`
- **Details/Legend**: `customer_segment`
- **Size**: `Count(customerid)`
- **Highlight**: Draw attention (via conditional formatting or a reference line) to the **High-Flight-Risk** segment (High Value + High Risk).

### Segment Detail Table
Columns: `customer_segment`, `Count(customerid)`, `Churn Rate`, `Average(monthly_charges)`, `Average(tenure_months)`

---

## PAGE 4 — CUSTOMER RISK EXPLORER

### Filterable Customer Table
Columns: 
- `customerid`
- `churn_probability` (Conditional formatting: Data bars, Red)
- `risk_level` (Conditional formatting: Critical=Dark Red, High=Red, Medium=Yellow, Low=Green)
- `customer_segment`
- `contract`
- `tenure_months`
- `monthly_charges`
- `top_risk_factor`
- `recommended_action`

### Slicers
- `risk_level` (Filter down to Critical/High/Medium/Low)
- Sort the table by `churn_probability` descending.

---

## PAGE 5 — MODEL PERFORMANCE

Since Power BI is for business users, present static metrics loaded from `data/processed/model_comparison.csv` if available, or build out static text boxes summarizing the data science phase:
- **Selected Model**: Logistic Regression
- **Recall**: 85%+ (At optimized threshold 0.20)
- **Selected Threshold**: 0.20 (Business justification: Capturing silent churners is more valuable than saving on false-positive retention offers).
- **Confusion Matrix**: Use a Matrix visual showing Predicted vs Actual churn at the 0.20 threshold.

---

## PAGE 6 — EXPLAINABLE AI

### Individual Customer Explanation Layout
Select a single `customerid` using a dropdown slicer to filter this page.
Display Card Visuals in a vertical flow:
- `customerid`
- ↓
- `churn_probability`
- ↓
- `risk_level`
- ↓
- `top_risk_factor`
- ↓
- `recommended_action`

*Note: For full SHAP waterfall plots, embed a Python visual in Power BI using the `shap` library, passing the specific customer's features to the explainer.*

---
### Design Guidelines
- **Typography**: Use Segoe UI or DIN.
- **Color Palette**: Use a consistent, dark-themed or clean corporate palette. (e.g., Churned = #E74C3C, Retained = #2ECC71).
- **Interactivity**: Ensure cross-filtering is enabled so clicking a segment on Page 1 filters the rest of the page.
