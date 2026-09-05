# Statistical Analysis Findings

The following table summarizes the hypothesis testing conducted to determine the statistical significance of observed differences between churned and retained customers.

### Key Metrics Explained
- **P-value**: The probability of obtaining test results at least as extreme as the results actually observed, under the assumption that the null hypothesis is correct. (Threshold = 0.05)
- **Effect Size**: Measures the magnitude of the difference (e.g., Cramer's V for Chi-Square, Rank-Biserial Correlation for Mann-Whitney).
- **Confidence Interval**: The range of values that we can be 95% confident contains the true difference between groups.

## Results Summary

| Hypothesis | Test | Statistic | P-value | Effect Size | Confidence Interval | Significant? | Business Interpretation |
|------------|------|-----------|---------|-------------|---------------------|--------------|-------------------------|
| Monthly Charges vs Churn | Mann-Whitney U | U=6.00e+06 | 3.31e-54 | r=-0.242 | [13.88, 17.90] | Yes | Churned customers have significantly higher monthly charges. High-spend customers are at higher risk. |
| Tenure vs Churn | Mann-Whitney U | U=2.52e+06 | 2.42e-208 | r=0.480 | [-30.00, -26.00] | Yes | Churned customers have significantly lower tenure. Early lifecycle is the high-risk window. |
| Total Charges vs Churn | Mann-Whitney U | U=3.38e+06 | 5.69e-83 | r=0.301 | [-1081.11, -855.88] | Yes | Retained customers have significantly higher total charges, driven entirely by their longer tenure. |
| Contract Type vs Churn | Chi-Square | Chi2=1184.60 | 5.86e-258 | V=0.410 | nan | Yes | Strong statistical association. Month-to-month contracts massively increase churn probability. |
| Payment Method vs Churn | Chi-Square | Chi2=648.14 | 3.68e-140 | V=0.303 | nan | Yes | Significant association. Electronic check is highly associated with churn. |
| Tech Support vs Churn (Internet Only) | Chi-Square / Z-test | Chi2=414.25 | 4.35e-92 | V=0.274 | Diff CI: [0.242, 0.287] | Yes | Customers without Tech Support churn at significantly higher rates. Lack of support drives attrition. |
| Internet Service vs Churn | Chi-Square | Chi2=732.31 | 9.57e-160 | V=0.322 | nan | Yes | Fiber optic customers churn significantly more than DSL customers, indicating possible competitive or pricing issues. |


### Important Note
Statistical significance indicates that the observed differences are highly unlikely to be due to random chance. However, this does **not** imply causation. Business context and common sense should guide any interventions.
