from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.database.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True, nullable=False)
    
    # Store just the minimal demographic/contract data needed for history/reports
    # We do NOT store sensitive PII here (e.g. precise lat_long is kept out unless explicitly needed)
    tenure_months = Column(Integer, nullable=True)
    contract = Column(String, nullable=True)
    monthly_charges = Column(Float, nullable=True)
    
    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="customer")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Prediction Outputs
    churn_probability = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    top_risk_factor = Column(String, nullable=True)
    protective_factors = Column(String, nullable=True)
    recommended_action = Column(String, nullable=True)
    
    # We can link the specific model version used
    model_version = Column(String, default="1.0.0")
    
    customer = relationship("Customer", back_populates="predictions")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    roc_auc = Column(Float, nullable=True)
    pr_auc = Column(Float, nullable=True)
    optimal_threshold = Column(Float, nullable=True)
    is_active = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
