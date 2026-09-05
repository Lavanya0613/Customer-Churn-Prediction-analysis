# Power BI Implementation Guide: Customer Churn Intelligence

This document outlines the architecture, data modeling, and visualization setup for the Telco Customer Churn Power BI Dashboard.

## Dataset Location
Load the flattened, analysis-ready dataset from:
`data/processed/powerbi_dashboard_data.csv`

## Recommended DAX Measures
Create the following DAX measures before building the visuals to ensure dynamic, cross-filterable metrics:

```dax
Total Customers = COUNTROWS('powerbi_dashboard_data')

Churned Customers = CALCULATE(COUNTROWS('powerbi_dashboard_data'), 'powerbi_dashboard_data'[Churn] = "Yes")

Churn Rate = DIVIDE([Churned Customers], [Total Customers], 0)

Avg Monthly Charges = AVERAGE('powerbi_dashboard_data'[Monthly Charges])

Avg Tenure = AVERAGE('powerbi_dashboard_data'[Tenure])

High Risk Customers = CALCULATE([Total Customers], 'powerbi_dashboard_data'[Risk Level] IN {"High Risk", "Critical Risk"})
```

---

## Dashboard Architecture

### PAGE 1: Executive Overview
**Objective**: Provide a high-level summary of business health and customer retention.

* **Visual 1**: Scorecards (Cards)
  * **Fields**: `[Total Customers]`, `[Churn Rate]`, `[High Risk Customers]`, `[Avg Tenure]`
  * **Business Question**: What is the overall health of the customer base?
* **Visual 2**: Donut Chart (Churn by Contract Type)
  * **Fields**: Axis: `Contract`, Values: `[Total Customers]`
  * **Business Question**: How does commitment length impact customer volume?
* **Visual 3**: Stacked Column Chart (Churn Rate by Customer Segment)
  * **Fields**: Axis: `Customer Segment`, Values: `[Churn Rate]`
  * **Business Question**: Which persona segments are most likely to leave?
* **Visual 4**: Line Chart (Tenure vs. Churn Rate)
  * **Fields**: Axis: `Tenure` (binned into years), Values: `[Churn Rate]`
  * **Business Question**: At what point in the customer lifecycle do we lose the most users?

### PAGE 2: Churn Drivers
**Objective**: Deep-dive into specific operational metrics impacting churn.

* **Visual 1**: Matrix (Subscription & Support vs Churn)
  * **Fields**: Rows: `Subscription`, Columns: `Support Activity`, Values: `[Churn Rate]`
  * **Business Question**: Does tech support mitigate the risk of high-speed (Fiber) churn?
* **Visual 2**: Scatter Plot (Monthly Charges vs Tenure)
  * **Fields**: X: `[Avg Tenure]`, Y: `[Avg Monthly Charges]`, Details: `Customer ID`, Legend: `Churn`
  * **Business Question**: Is there a correlation between high spending, short tenure, and churn?
* **Visual 3**: Bar Chart (Churn by Payment Method)
  * **Fields**: Axis: `Payment Method`, Values: `[Churn Rate]`
  * **Business Question**: Are customers on manual payment methods (Electronic Check) more prone to churn?

### PAGE 3: Customer Risk
**Objective**: Actionable list for Customer Success representatives to target interventions.

* **Visual 1**: Table (High-Risk Intervention List)
  * **Fields**: `Customer ID`, `Churn Probability`, `Risk Level`, `Top Risk Factor`, `Recommended Action`
  * **Filters**: Filter `Risk Level` to "High Risk" and "Critical Risk" only. Sort by `Churn Probability` Descending.
  * **Business Question**: Who should we call today, why are they leaving, and what should we offer them?
* **Visual 2**: Tree Map (Top Risk Factors Distribution)
  * **Fields**: Category: `Top Risk Factor`, Values: `[High Risk Customers]`
  * **Business Question**: What is the most common reason our at-risk customers are flagged?
* **Visual 3**: Slicer Panel
  * **Fields**: `Customer Segment`, `Contract`, `Risk Level`
  * **Business Question**: Allows reps to filter the intervention list to their specific territory or domain.

### PAGE 4: Model Performance
**Objective**: Technical overview for data science and leadership on model reliability.
*(Note: As PBI is a BI tool, model evaluation metrics should be inputted as static text cards or simple tables derived from the Python evaluation phase, unless importing the raw test-set predictions).*

* **Visual 1**: Multi-Row Card (Key Metrics)
  * **Fields**: Input metrics manually or via a secondary metadata table (e.g., ROC-AUC: 0.84, PR-AUC: 0.65).
  * **Business Question**: Is the model accurately identifying churners?
* **Visual 2**: 100% Stacked Bar Chart (Risk Level Calibration)
  * **Fields**: Axis: `Risk Level`, Legend: `Churn` (Actual), Values: `[Total Customers]`
  * **Business Question**: What percentage of customers flagged as "Critical Risk" actually churned? (Tests precision/calibration).
* **Visual 3**: Text Box (Threshold Strategy)
  * **Text**: Explain the cost-matrix threshold (Critical >= 0.50, High >= 0.20) based on $100 False Negative vs $20 False Positive cost.
  * **Business Question**: Why are some customers with a 30% probability flagged as "High Risk"?

---
**Design Note**: 
Use a consistent color palette matching the React frontend (e.g., Critical Risk = Red `#EF4444`, High Risk = Yellow `#F59E0B`, Low Risk = Green `#10B981`). Ensure all charts have clear, non-technical titles.
