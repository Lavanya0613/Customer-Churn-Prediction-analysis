# Deployment Plan & Architecture Review

This document outlines the final production-readiness review and the recommended cloud deployment architecture for the Telco Customer Churn Intelligence System.

---

## 1. Production-Readiness Review

### Architecture Checks
* **Environment Variables**: Confirmed. All configuration is read from the OS environment, falling back to sensible defaults.
* **Secrets Management**: Confirmed. No hardcoded database credentials, API keys, or secrets are tracked in version control. `.env.example` serves as the safe template.
* **CORS (Cross-Origin Resource Sharing)**: **[ACTION REQUIRED]** Currently set to `allow_origins=["*"]` for local development. Before deploying, this must be updated in `api/main.py` to exclusively allow the production frontend domain.
* **API Configuration**: Confirmed. FastAPI utilizes a `lifespan` manager for graceful startup/shutdown.
* **Database Configuration**: Confirmed. SQLAlchemy connection pool is configured safely via ORM, preventing SQL injection.
* **Model Loading**: Confirmed. Machine Learning artifacts (`.pkl`) are loaded exactly once into a Singleton `ModelService` via the server startup hook, preventing memory exhaustion.
* **Logging**: Confirmed. Standard Python `logging` module writes critical events (startup, inference errors, db errors) to stdout/stderr for container orchestrators to pick up.
* **Error Handling**: Confirmed. FastAPI globally catches unhandled exceptions and safely returns `HTTP 500` rather than crashing the event loop.
* **Docker Configuration**: Confirmed. The frontend uses a multi-stage Vite->Nginx build (tiny footprint), and the backend uses an optimized Python slim image.
* **Frontend API URL**: Confirmed. Vite consumes `VITE_API_URL` dynamically from the environment.
* **Health Endpoint**: Confirmed. `GET /health` acts as the liveness probe for Docker/Cloud load balancers.
* **Security Basics**: Confirmed. React natively escapes XSS, and SQLAlchemy parameterized queries prevent SQL injection.
* **Dependency Versions**: Confirmed. `requirements.txt` strictly pins versions (e.g., `scikit-learn==1.5.1`, `pandas==2.2.2`) ensuring reproducible builds.

---

## 2. Cloud Deployment Architecture (Portfolio-Optimized)

To demonstrate full-stack deployment capability without incurring unnecessary cloud costs or complex Kubernetes management, a **PaaS (Platform as a Service)** architecture is recommended. 

### Recommended Stack
1. **Frontend**: Vercel or Netlify (Free Tier)
2. **Backend**: Render Web Service or Heroku (Free/Hobby Tier)
3. **Database**: Render PostgreSQL or Supabase (Free Tier)
4. **ML Model**: Bundled inside the Backend Docker container

### Component Strategy

#### A. PostgreSQL Database (Supabase / Render)
* **Why**: Managed, serverless Postgres is easier to maintain than a stateful VM.
* **Steps**: 
  1. Provision a free Postgres database.
  2. Retrieve the remote `DATABASE_URL`.
  3. No need to run migrations manually; FastAPI will auto-initialize tables on its first startup.

#### B. FastAPI + ML Backend (Render)
* **Why**: Render natively supports Dockerfile deployments with zero configuration.
* **Steps**:
  1. Connect your GitHub repository to Render.
  2. Create a new "Web Service" pointing to `backend.Dockerfile`.
  3. Set Environment Variable: `DATABASE_URL` (from the step above).
  4. Render will build the container, install ML dependencies, load the model, and expose the API via a public HTTPS URL (e.g., `https://telco-api.onrender.com`).

#### C. React Frontend (Vercel)
* **Why**: Vercel is the gold standard for Vite/React deployments with instant global CDN caching.
* **Steps**:
  1. Connect your GitHub repository to Vercel.
  2. Set Root Directory to `frontend/`.
  3. Set Environment Variable: `VITE_API_URL` = `https://telco-api.onrender.com`.
  4. Vercel will build and deploy the React UI to a public HTTPS domain.

---

## 3. Final Pre-Flight Checklist

Before executing the deployment, complete these steps:
- [ ] Update `CORS` origins in `api/main.py` from `*` to the Vercel frontend URL once known.
- [ ] Push the entire codebase to a public/private GitHub repository.
- [ ] Provision the cloud PostgreSQL database.
- [ ] Connect Render and Vercel to the repository.
