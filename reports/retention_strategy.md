# Retention Opportunity Analytics Strategy

Our Customer Churn Intelligence platform has been expanded from purely identifying churn probability ("Who will churn?") to actionable retention prioritization ("Which customers should the business prioritize?").

## The 2x2 Retention Priority Matrix

To maximize Return on Retention Investment (ROZI), we analyze our customer base through two dimensions:
1. **Customer Value Proxy**: We use the native `cltv` (Customer Lifetime Value) metric provided in the dataset. The median CLTV in our customer base is approximately $4,500. We define customers above this threshold as **High Value**.
2. **Churn Risk**: Based on our optimized predictive modeling threshold, any customer with a churn probability > 20% is classified as **High Risk**.

This yields four distinct retention quadrants:

```text
                     HIGH VALUE (CLTV > $4500)
                                 │
           PROACTIVE             │      PRIORITY
           ENGAGEMENT            │      RETENTION
                                 │
        ─────────────────────────┼─────────────────────────
                                 │
           MONITOR               │      STANDARD
           (LOW PRIORITY)        │      RETENTION
                                 │
                     LOW VALUE (CLTV <= $4500)
```

## Strategy by Quadrant

### 1. Priority Retention (Top Right)
**Profile:** High Value + High Risk
**Strategic Goal:** Protect Immediately
**Action:** These customers represent the highest risk to top-line revenue. They should be routed immediately to specialized retention or Customer Success agents. They warrant high-cost interventions such as significant subscription discounts, free hardware upgrades, or personalized executive outreach.

### 2. Standard Retention (Bottom Right)
**Profile:** Low Value + High Risk
**Strategic Goal:** Retain Efficiently
**Action:** While these customers are at high risk of leaving, their lower CLTV means expensive interventions will destroy margin. Retention strategies here should be automated and low-touch: email marketing campaigns, self-service downgrade options, or standard automated save-offers.

### 3. Proactive Engagement (Top Left)
**Profile:** High Value + Low Risk
**Strategic Goal:** Maximize Loyalty & Expansion
**Action:** These customers are highly valuable and currently safe. Retention efforts here focus on proactive relationship building. We recommend upsell/cross-sell campaigns (e.g., adding Tech Support or Online Security) and VIP loyalty programs to keep their satisfaction high.

### 4. Monitor (Bottom Left)
**Profile:** Low Value + Low Risk
**Strategic Goal:** Maintain Efficiency
**Action:** These customers are low priority. No active retention resources should be spent here. Simply monitor their usage and risk score over time.

## Operational Integration

This matrix logic has been integrated into the core product architecture:
- **API**: The `/predict` endpoints now return a `retention_priority` string alongside the raw probability.
- **Frontend Dashboard**: The React Risk Table displays the Retention Priority, color-coded to draw attention to Priority Retention customers.
- **Power BI Dashboard**: The underlying dashboard dataset now includes `retention_priority` as a slicer and dimension, allowing executives to filter pipeline metrics by retention urgency.
