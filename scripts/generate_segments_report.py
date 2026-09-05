import pandas as pd
import os

def generate_report():
    df = pd.read_csv('data/processed/segmentation_summary.csv')
    
    report_content = """# Customer Segmentation Analysis

This report outlines the meaningful customer groups identified through K-Means clustering, built upon core business drivers such as tenure, monthly charges, and service adoption (Tech Support/Online Security, Contract type). The target variable (Churn) was **strictly excluded** from the clustering process to prevent data leakage and ensure objective segment discovery.

## K-Means Cluster Profiles (K=4)

| Segment | Customers | % of Base | Avg Tenure | Avg Monthly Charges | Churn Rate | Risk | Business Interpretation |
|---------|-----------|-----------|------------|---------------------|------------|------|-------------------------|
"""
    
    for _, row in df.iterrows():
        report_content += f"| {row['ml_segment']} | {row['Customers']} | {row['% of Base']}% | {row['Avg_Tenure']:.1f} mo | ${row['Avg_Monthly_Charges']:.2f} | {row['Churn_Rate']:.1%} | **{row['Risk']}** | {row['Business Interpretation']} |\n"
        
    report_content += """

## Key Segment Takeaways

- **Highest-Risk Segment**: *High-Flight-Risk (Premium, M2M)*. These customers have short tenures, high monthly charges, and operate on month-to-month contracts. They churn at extremely high rates and require immediate, targeted retention campaigns (e.g., discounts for 1-year commitments).
- **Highest-Value Segment**: *Premium Loyalists*. High spenders with long tenures. They provide the core revenue stability for the business and have very low churn risk.
- **Highest-Value / Highest-Risk Intersection**: The *High-Flight-Risk* segment brings in significant monthly revenue (Premium pricing) but leaves too quickly to yield high Customer Lifetime Value. Converting them to *Premium Loyalists* is the primary business optimization opportunity.
- **Low-Engagement Customers**: *Uncommitted Budget* customers cost very little but also have low engagement. They churn quickly, likely because they find cheaper alternatives or no longer need the basic service.
"""

    os.makedirs('reports', exist_ok=True)
    with open('reports/customer_segments.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print("Report generated at reports/customer_segments.md")

if __name__ == "__main__":
    generate_report()
