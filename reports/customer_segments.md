# Customer Segmentation Analysis

This report outlines the meaningful customer groups identified through K-Means clustering, built upon core business drivers such as tenure, monthly charges, and service adoption (Tech Support/Online Security, Contract type). The target variable (Churn) was **strictly excluded** from the clustering process to prevent data leakage and ensure objective segment discovery.

## K-Means Cluster Profiles (K=4)

| Segment | Customers | % of Base | Avg Tenure | Avg Monthly Charges | Churn Rate | Risk | Business Interpretation |
|---------|-----------|-----------|------------|---------------------|------------|------|-------------------------|
| High-Flight-Risk (Premium, M2M) | 3083 | 43.8% | 15.4 mo | $64.09 | 46.2% | **High** | Premium, month-to-month users with high churn risk. Need immediate intervention. |
| Uncommitted Budget | 1085 | 15.4% | 34.7 mo | $75.13 | 22.0% | **Medium** | New, low-cost users. High churn but low revenue impact. |
| Premium Loyalists | 1473 | 20.9% | 55.4 mo | $84.28 | 8.6% | **Low** | Long-term engaged users with support add-ons. Very stable. |
| Engaged Security/Support Users | 1402 | 19.9% | 43.8 mo | $37.71 | 5.7% | **Low** | High value, highly loyal core customer base. |


## Key Segment Takeaways

- **Highest-Risk Segment**: *High-Flight-Risk (Premium, M2M)*. These customers have short tenures, high monthly charges, and operate on month-to-month contracts. They churn at extremely high rates and require immediate, targeted retention campaigns (e.g., discounts for 1-year commitments).
- **Highest-Value Segment**: *Premium Loyalists*. High spenders with long tenures. They provide the core revenue stability for the business and have very low churn risk.
- **Highest-Value / Highest-Risk Intersection**: The *High-Flight-Risk* segment brings in significant monthly revenue (Premium pricing) but leaves too quickly to yield high Customer Lifetime Value. Converting them to *Premium Loyalists* is the primary business optimization opportunity.
- **Low-Engagement Customers**: *Uncommitted Budget* customers cost very little but also have low engagement. They churn quickly, likely because they find cheaper alternatives or no longer need the basic service.
