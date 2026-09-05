import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.database import Base
from api.database.models import Customer, Prediction
from api.database.crud import save_prediction

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_save_prediction(db):
    cust_data = {
        "customerid": "TEST-DB-123",
        "tenure_months": 24,
        "contract": "One year",
        "monthly_charges": 55.0
    }
    
    pred_data = {
        "churn_probability": 0.85,
        "risk_level": "High Risk",
        "top_risk_factor": "tenure_months",
        "protective_factors": "None",
        "recommended_action": "Review pricing"
    }
    
    # Save first time
    db_pred = save_prediction(db, cust_data, pred_data)
    
    assert db_pred.id is not None
    assert db_pred.churn_probability == 0.85
    
    # Check customer was created
    customer = db.query(Customer).filter(Customer.customer_id == "TEST-DB-123").first()
    assert customer is not None
    assert customer.tenure_months == 24
    
    # Save second time (should use same customer)
    db_pred2 = save_prediction(db, cust_data, pred_data)
    
    customers = db.query(Customer).all()
    assert len(customers) == 1 # Still only one customer
