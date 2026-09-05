from pydantic import BaseModel, Field
from typing import Optional, List

class CustomerFeatureInput(BaseModel):
    customerid: Optional[str] = Field("UNKNOWN", description="Customer ID")
    country: str = Field("United States", description="Country of the customer")
    state: str = Field("California", description="State of the customer")
    city: str = Field("Los Angeles", description="City of the customer")
    zip_code: int = Field(90001, description="Zip code")
    lat_long: str = Field("33.973616, -118.242766", description="Latitude and Longitude")
    latitude: float = Field(33.973616, description="Latitude")
    longitude: float = Field(-118.242766, description="Longitude")
    gender: str = Field("Male", description="Gender of the customer")
    senior_citizen: str = Field("No", description="Is the customer a senior citizen (Yes/No)")
    partner: str = Field("No", description="Does the customer have a partner (Yes/No)")
    dependents: str = Field("No", description="Does the customer have dependents (Yes/No)")
    tenure_months: int = Field(..., description="Number of months with the company")
    phone_service: str = Field("Yes", description="Has phone service (Yes/No)")
    multiple_lines: str = Field("No", description="Has multiple lines (Yes/No/No phone service)")
    internet_service: str = Field("Fiber optic", description="Internet service type")
    online_security: str = Field("No", description="Has online security (Yes/No/No internet service)")
    online_backup: str = Field("No", description="Has online backup (Yes/No/No internet service)")
    device_protection: str = Field("No", description="Has device protection (Yes/No/No internet service)")
    tech_support: str = Field("No", description="Has tech support (Yes/No/No internet service)")
    streaming_tv: str = Field("No", description="Has streaming TV (Yes/No/No internet service)")
    streaming_movies: str = Field("No", description="Has streaming movies (Yes/No/No internet service)")
    contract: str = Field("Month-to-month", description="Contract type")
    paperless_billing: str = Field("Yes", description="Has paperless billing (Yes/No)")
    payment_method: str = Field("Electronic check", description="Payment method")
    monthly_charges: float = Field(70.0, description="Monthly charges")
    total_charges: float = Field(70.0, description="Total lifetime charges")
    cltv: float = Field(5000.0, description="Customer Lifetime Value")
    
    class Config:
        schema_extra = {
            "example": {
                "customerid": "1234-ABCD",
                "country": "United States",
                "state": "California",
                "city": "Los Angeles",
                "zip_code": 90001,
                "lat_long": "33.973616, -118.242766",
                "latitude": 33.973616,
                "longitude": -118.242766,
                "gender": "Female",
                "senior_citizen": "No",
                "partner": "Yes",
                "dependents": "Yes",
                "tenure_months": 24,
                "phone_service": "Yes",
                "multiple_lines": "No",
                "internet_service": "DSL",
                "online_security": "Yes",
                "online_backup": "Yes",
                "device_protection": "No",
                "tech_support": "Yes",
                "streaming_tv": "No",
                "streaming_movies": "No",
                "contract": "One year",
                "paperless_billing": "No",
                "payment_method": "Credit card (automatic)",
                "monthly_charges": 65.5,
                "total_charges": 1572.0,
                "cltv": 4500.0
            }
        }

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_level: str
    top_risk_factor: str
    protective_factors: str
    recommended_action: str
    retention_priority: str

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
