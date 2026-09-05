# Exploratory Data Analysis Insights

## Customer Base Overview
- **Total Customers**: 7,043
- **Global Churn Rate**: 26.5%
- **Average Monthly Revenue (MRR)**: $64.76
- **Average Tenure**: 32.4 months

## Business Questions & Findings

### 1. Which contract types suffer the most churn?
- **Chart**: Churn Rate by Contract Type (Dual-axis Bar/Line)
- **Observation**: Month-to-month contracts have a drastically higher churn rate (~42.7%) compared to 1-year (11.2%) and 2-year (2.8%) contracts.
- **Business Interpretation**: Long-term commitments heavily lock in customers. Moving customers to annual plans (even at a slight discount) should be a primary retention strategy.
- **Limitation**: Observational data. Customers who intend to stay might self-select into longer contracts, rather than the contract itself causing them to stay.

### 2. How does payment method impact churn?
- **Chart**: Churn Rate by Payment Method
- **Observation**: Electronic check is associated with the highest churn rate (~45%), far above automatic payment methods (credit card or bank transfer, ~15-16%).
- **Business Interpretation**: Friction in payment or the conscious act of paying manually every month reminds customers of the cost, prompting re-evaluation. Pushing automatic payments could naturally reduce churn.
- **Limitation**: Correlation, not causation. Customers with less stable finances might prefer manual checks and inherently have higher churn.

### 3. Does tenure differ between churned and retained customers?
- **Chart**: Tenure Distribution by Churn Status (KDE plot)
- **Observation**: Churn is heavily right-skewed, meaning it happens primarily in the first few months (1-5 months). Retained customers show a large peak at the highest tenure (70+ months).
- **Business Interpretation**: The onboarding phase is the most critical period. If a customer survives the first 6 months, their likelihood of churning drops significantly.
- **Limitation**: Survivor bias. 

### 4. How do monthly charges correlate with churn?
- **Chart**: Monthly Charges Distribution by Churn Status
- **Observation**: Churned customers have a bimodal distribution with a large peak around $70-$100/month. Retained customers are concentrated heavily at the ~$20/month mark.
- **Business Interpretation**: High-spending customers are at significantly higher risk of leaving, likely due to price sensitivity or competition offering cheaper premium bundles.
- **Limitation**: We lack data on competitor pricing to prove price sensitivity.

### 5. What are the strongest categorical drivers of churn?
- **Chart**: Top Categorical Drivers (Bar chart of max churn difference)
- **Observation**: Contract (Month-to-month vs Two year), Online Security (No vs Yes), and Tech Support (No vs Yes) have the largest absolute differences in churn rate.
- **Business Interpretation**: Customers without security and tech support add-ons churn much faster. Bundling these services for free in the first 3 months could improve retention.

### 6. Are there significant outliers in the data?
- **Chart**: Boxplots for Monthly Charges and Tenure
- **Observation**: There are no statistical outliers beyond the whiskers in either `monthly_charges` or `tenure_months`.
- **Business Interpretation**: The data falls within expected bounded ranges (tenure max ~72 months, charges max ~$120). No outlier removal or clipping is necessary.

### 7. Is there multicollinearity among numerical features?
- **Chart**: Correlation Heatmap
- **Observation**: `tenure` and `total_charges` are highly correlated (0.83).
- **Business Interpretation**: This is mathematically expected since total = monthly * tenure. We should drop `total_charges` during modeling to prevent multicollinearity and stabilize feature importance.
