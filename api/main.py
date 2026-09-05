import logging
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from typing import List, Optional
import os

from sqlalchemy.orm import Session
from fastapi import Depends
from api.database import models, crud
from api.database.database import engine, get_db

from fastapi.middleware.cors import CORSMiddleware

from api.schemas import CustomerFeatureInput, PredictionResponse, BatchPredictionResponse
from api.services import model_service
from api.routers import analytics

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Model loading at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading ML models and preprocessors...")
    try:
        model_service.load_models()
        logger.info("Models loaded successfully.")
        
        # Initialize database schema
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database initialized.")
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        raise e
    yield
    logger.info("Shutting down API and cleaning up resources...")

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Production API for scoring customer churn risk and generating retention recommendations.",
    version="1.0.0",
    lifespan=lifespan
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost"], # Added localhost for docker-compose setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics.router)

@app.get("/health", tags=["System"])
async def health_check():
    """Check if the API and models are loaded and healthy."""
    if model_service.predictor is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Models not loaded")
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/model-info", tags=["System"])
async def model_info():
    """Get information about the currently loaded model."""
    if model_service.predictor is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Models not loaded")
    return {
        "model_type": "Logistic Regression",
        "features": list(model_service.explainer.feature_names),
        "thresholds": {
            "optimal": model_service.predictor.OPTIMAL_THRESHOLD,
            "critical": model_service.predictor.CRITICAL_THRESHOLD
        }
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_churn(
    customer: CustomerFeatureInput, 
    save: bool = False,
    db: Session = Depends(get_db)
):
    """Predict churn risk for a single customer."""
    try:
        cust_dict = customer.model_dump()
        result = model_service.predict_single(cust_dict)
        
        if save:
            crud.save_prediction(db=db, customer_data=cust_dict, prediction=result)
            
        return result
    except ValueError as ve:
        logger.error(f"Validation error during prediction: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal server error during prediction: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during prediction")

@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_churn_batch(
    customers: List[CustomerFeatureInput],
    save: bool = False,
    db: Session = Depends(get_db)
):
    """Predict churn risk for a batch of customers."""
    if not customers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty customer list")
    
    try:
        customers_data = [c.model_dump() for c in customers]
        results = model_service.predict_batch(customers_data)
        
        if save:
            for cust_data, pred in zip(customers_data, results):
                crud.save_prediction(db=db, customer_data=cust_data, prediction=pred)
                
        return {"predictions": results}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal server error during batch prediction: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during batch prediction")

@app.get("/predictions/high-risk", tags=["Prediction"])
async def get_high_risk_predictions(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent high-risk predictions from the database."""
    try:
        preds = db.query(models.Prediction).join(models.Customer).filter(
            models.Prediction.risk_level.in_(["High Risk", "Critical Risk"])
        ).order_by(models.Prediction.churn_probability.desc()).limit(limit).all()
        
        return [
            {
                "customer_id": p.customer.customer_id,
                "churn_probability": p.churn_probability,
                "risk_level": p.risk_level,
                "top_risk_factor": p.top_risk_factor,
                "recommended_action": p.recommended_action
            }
            for p in preds
        ]
    except Exception as e:
        logger.error(f"Error fetching predictions: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
