# Live Operational Monitoring & Responsible-Use Stewardship Framework

## 1. Post-Deployment Monitoring Protocols

### Data & Feature Drift
* **Metric Metric:** Track the Population Stability Index (PSI) and Wasserstein Distance weekly on top features (`recency_days`, `ticket_count_90d`, `sessions_30d`).
* **Threshold Rule:** If $\text{PSI} > 0.25$ occurs across two consecutive monitoring logs, trigger an automated data curation run for model retraining.

### Prediction Distribution Analysis
* **Metric Metric:** Log the rolling ratio of positive predictions vs. stable customer profiles.
* **Threshold Rule:** Sudden shifts in the target positive rate (e.g., predicted churn rate jumping from a baseline of 15% up to 45%) with no sudden drops in app traffic indicate upstream data pipeline changes or broken API schemas.

### Business Value Audits
* **Metric Metric:** Measure true churn vs. false alarms using 60-day out-of-fold transactional validation logs.
* **Target KPI:** Maintain a minimum 15% reduction in overall churn velocity across targeted segments compared to our un-incentivized control group.

### API Operational Health
* **Metric Metric:** Monitor 5xx server exceptions, validation failures (422 HTTP responses), and p99 response times.
* **Target KPI:** P99 response times must remain below 45 milliseconds to keep CRM integration performance fast and lightweight.

---

## 2. Responsible-Use Framework & Guidelines

### ✅ Correct/Approved Applications
* **Proactive Service Restoration:** Use high risk scores to automatically escalate pending or unresolved customer service tickets to executive resolution teams.
* **Lifestyle Re-engagement:** Personalize marketing layouts to match a user's `preferred_category` when risk scores rise.
* **Loyalty Investment:** Offer priority shipping or premium tier upgrades to valuable customers showing early signs of dipping activity.

### ❌ Prohibited/Incorrect Applications
* **Margin Erosion via Broad Discounts:** Do not issue blanket, sitewide coupons to all high-risk users. This conditions organic shoppers to stop buying at full price.
* **Account Access Constraints:** Never lock accounts, downgrade membership benefits, or restrict customer support availability based on high predicted churn scores.
* **Automated Offboarding Decisions:** Do not drop customer outreach entirely or close accounts automatically based on model risk scores without a human manager review.
