import pandas as pd
import os

def generate_report():
    df = pd.read_csv('data/processed/statistical_summary.csv')
    
    report_content = """# Statistical Analysis Findings

The following table summarizes the hypothesis testing conducted to determine the statistical significance of observed differences between churned and retained customers.

### Key Metrics Explained
- **P-value**: The probability of obtaining test results at least as extreme as the results actually observed, under the assumption that the null hypothesis is correct. (Threshold = 0.05)
- **Effect Size**: Measures the magnitude of the difference (e.g., Cramer's V for Chi-Square, Rank-Biserial Correlation for Mann-Whitney).
- **Confidence Interval**: The range of values that we can be 95% confident contains the true difference between groups.

## Results Summary

| Hypothesis | Test | Statistic | P-value | Effect Size | Confidence Interval | Significant? | Business Interpretation |
|------------|------|-----------|---------|-------------|---------------------|--------------|-------------------------|
"""
    
    for _, row in df.iterrows():
        pval_str = f"{row['P-value']:.2e}" if row['P-value'] < 0.001 else f"{row['P-value']:.4f}"
        
        report_content += f"| {row['Hypothesis']} | {row['Test']} | {row['Statistic']} | {pval_str} | {row['Effect Size']} | {row['Confidence Interval']} | {row['Significant?']} | {row['Business Interpretation']} |\n"
        
    report_content += """

### Important Note
Statistical significance indicates that the observed differences are highly unlikely to be due to random chance. However, this does **not** imply causation. Business context and common sense should guide any interventions.
"""

    os.makedirs('reports', exist_ok=True)
    with open('reports/statistical_findings.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print("Report generated at reports/statistical_findings.md")

if __name__ == "__main__":
    generate_report()
