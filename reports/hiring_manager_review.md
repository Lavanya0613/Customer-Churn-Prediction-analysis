# Senior Data Scientist / Hiring Manager Project Review

As a hiring manager, I review hundreds of portfolios. Here is a brutally honest, critical evaluation of your Customer Churn Intelligence project.

---

## 1. Category Evaluations & Scoring

### Data Science & Analytics
1. **Business problem (9/10)**: Excellent framing. Tying churn to Customer Lifetime Value (CLTV) and explicitly calculating a cost-matrix ($100 FN vs $20 FP) shows strong commercial awareness, which most juniors lack.
2. **Data quality (7/10)**: Standard handling of missing `TotalCharges`. However, you did not rigorously check for or document extreme outliers (e.g., impossible tenures) or perform deep data-type stress testing beyond the obvious.
3. **EDA quality (8/10)**: Good univariate/bivariate analysis, but lacked multivariate interaction plots (e.g., does High Spend + Fiber Optic + Short Tenure = guaranteed churn?).
4. **Statistical reasoning (7/10)**: Used Mann-Whitney and Chi-Square, which is good. But correlation matrices often ignore the assumptions of linearity. Did you check for multicollinearity (VIF) between `Tenure` and `TotalCharges` before feeding them into Logistic Regression?
5. **Feature engineering (6/10)**: Basic. `service_count` and `spend_delta` are okay, but you missed temporal features (e.g., estimated time until contract renewal) which are the strongest predictors of churn.
6. **Leakage prevention (9/10)**: Strong. Using `sklearn.pipeline.Pipeline` with `train_test_split` is the correct, production-grade way to prevent scaling/imputation leakage.
7. **ML methodology (6/10)**: Weak. You evaluated a few models but skipped rigorous cross-validation (K-Fold) and extensive hyperparameter tuning (GridSearchCV/Optuna). The model choice was good, but the tuning was superficial.
8. **Model evaluation (8/10)**: Good use of PR-AUC alongside ROC-AUC, recognizing that class imbalance makes standard accuracy misleading.
9. **Threshold selection (10/10)**: Flawless. Rejecting the default 0.5 threshold in favor of a 0.20 threshold derived from a business cost matrix is senior-level thinking.
10. **Explainability (8/10)**: Good use of SHAP. However, claiming causal recommendations ("Offer annual contract") based on SHAP (which is correlational) is a slight methodological overstep.

### Engineering & Deployment
11. **Customer segmentation (7/10)**: Good conceptual grouping, but K-Means on just two variables is overly simplistic for a real-world scenario.
12. **Business recommendations (7/10)**: Hardcoded rules mapping to risk tiers are practical, but static. Real systems use uplift modeling or reinforcement learning for next-best-action.
13. **API architecture (8/10)**: FastAPI with Pydantic schemas and `lifespan` model loading is exactly how it should be done. Missing authentication/API keys.
14. **Database design (7/10)**: Good use of SQLAlchemy and basic deduplication (`get_or_create`). Missing a migration framework (like Alembic). Database schema is slightly denormalized.
15. **Frontend (8/10)**: Clean, functional React UI. Great use of env variables (`VITE_API_URL`). But it lacks state management (Redux/Zustand) for scaling and has zero frontend tests (Jest/Cypress).
16. **Power BI dashboard (8/10)**: Solid denormalized schema design for BI. Providing DAX and wireframes is highly practical.
17. **Docker (9/10)**: Excellent multi-stage builds and `docker-compose`. Using Nginx for the frontend and a slim image for Python is production-standard.
18. **Testing (5/10)**: Weak area. 7 backend tests are better than nothing, but it lacks ML unit tests (e.g., testing data drift, model invariants) and frontend tests.
19. **Documentation (9/10)**: The README is phenomenal. It targets the right personas and distinguishes experimentation from deployment.
20. **GitHub quality (8/10)**: Good structure. Missing CI/CD pipelines (GitHub Actions) to run those tests automatically on push.

---

## 2. Resume Impact

**"Would this project strengthen a Data Analyst resume?"**
**Yes, strongly.** The Power BI data modeling, SQL/database integration, EDA, and statistical testing demonstrate you can do more than just build dashboards; you can drive actionable insights.

**"Would this project strengthen a Data Scientist resume?"**
**Yes, but expect grilling.** You nailed the business framing and deployment, which sets you apart. However, a senior DS will challenge your lack of hyperparameter tuning, cross-validation, and causal inference. You must be prepared to defend why you prioritized a deployed MVP over a perfectly tuned model.

**"Would this project demonstrate ML Engineering ability?"**
**Yes, mostly.** The FastAPI, Docker, and SQLAlchemy integration is exactly what ML Engineers do. To be a true MLE project, it needs CI/CD, model registry (MLflow), and automated retraining pipelines (Airflow/Prefect).

---

## 3. Interview Preparation

**"What would an interviewer challenge me on?"**
1. **Multicollinearity**: "You used Logistic Regression. `Tenure` and `TotalCharges` are almost perfectly correlated. How did this impact your model coefficients, and did you handle it?"
2. **Causality vs Correlation**: "You recommended offering annual contracts to high-risk month-to-month users. But did they churn *because* of the contract, or did they pick that contract *because* they intended to leave soon?"
3. **Data Drift**: "How would you know if this model stops working 6 months from now in production?"

**"What questions should I be prepared to answer?"**
* "Walk me through exactly how you calculated that 0.20 threshold."
* "Why did you choose FastAPI over Flask or Django?"
* "If this dataset was 500 million rows instead of 7,000, what tools in your pipeline would break first, and how would you replace them?"

---

## 4. TOP 10 Improvements for Maximum Portfolio Impact

If you want to take this from a "Great" project to a "Top 1% Senior" project, implement these:

1. **Add GitHub Actions (CI/CD)**: Write a `.github/workflows/main.yml` that runs your `pytest` suite and builds the Docker images automatically on every push.
2. **Handle Multicollinearity**: Drop `TotalCharges` (as it's just `Tenure * MonthlyCharges`) or apply PCA, and document this explicitly to satisfy strict statisticians.
3. **Implement Cross-Validation**: Refactor the training script to use `StratifiedKFold` and `GridSearchCV` to prove your model isn't overfitting a single random seed.
4. **Add Alembic**: Introduce database migrations for SQLAlchemy. It proves you know how databases evolve in production.
5. **Add ML Unit Tests**: Write tests that assert model constraints (e.g., `test_female_and_male_have_similar_mean_predictions` to check for bias).
6. **Implement MLflow**: Add MLflow tracking to your training notebook to log parameters, metrics, and models. This screams "ML Engineer".
7. **Refine Segmentation**: Replace the basic 2-variable K-Means with an RFM (Recency, Frequency, Monetary) or DBScan approach, and evaluate with Silhouette scores.
8. **Add Authentication**: Secure the FastAPI endpoints with a basic JWT or API key middleware. 
9. **Frontend Testing**: Add just 2-3 React Testing Library tests for your main forms.
10. **Include a Data Drift Script**: Add a simple script (e.g., using `Evidently AI`) that compares the training data distribution to the Postgres inference data distribution to detect drift.
