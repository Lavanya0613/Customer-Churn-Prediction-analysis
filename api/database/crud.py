from sqlalchemy.orm import Session
from api.database import models
from api.schemas import PredictionResponse

def save_prediction(db: Session, customer_data: dict, prediction: dict):
    """
    Saves a prediction and ensures the customer exists in the database.
    """
    customer_id = customer_data.get('customerid', 'UNKNOWN')
    
    # 1. Get or create customer
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        db_customer = models.Customer(
            customer_id=customer_id,
            tenure_months=customer_data.get('tenure_months'),
            contract=customer_data.get('contract'),
            monthly_charges=customer_data.get('monthly_charges')
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        
    # 2. Save prediction
    db_prediction = models.Prediction(
        customer_id=db_customer.id,
        churn_probability=prediction.get('churn_probability'),
        risk_level=prediction.get('risk_level'),
        top_risk_factor=prediction.get('top_risk_factor'),
        protective_factors=prediction.get('protective_factors'),
        recommended_action=prediction.get('recommended_action')
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction
