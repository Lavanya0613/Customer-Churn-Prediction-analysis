from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(prefix="/analytics", tags=["analytics"])

ANALYTICS_FILE = os.path.join("data", "processed", "analytics_dashboard.json")

def load_analytics():
    if not os.path.exists(ANALYTICS_FILE):
        raise HTTPException(status_code=503, detail="Analytics data not available. Please run generate_analytics.py first.")
    with open(ANALYTICS_FILE, "r") as f:
        return json.load(f)

@router.get("/")
def get_all_analytics():
    """Returns the entire pre-computed analytics payload for the dashboard."""
    return load_analytics()

@router.get("/kpis")
def get_kpis():
    data = load_analytics()
    return data.get("kpis", {})

@router.get("/eda")
def get_eda():
    data = load_analytics()
    return {
        "churn_by_contract": data.get("churn_by_contract", []),
        "churn_by_internet": data.get("churn_by_internet", []),
        "tenure_dist_churned": data.get("tenure_dist_churned", []),
        "tenure_dist_retained": data.get("tenure_dist_retained", []),
        "charges_dist_churned": data.get("charges_dist_churned", []),
        "charges_dist_retained": data.get("charges_dist_retained", []),
        "correlation": data.get("correlation", [])
    }

@router.get("/segmentation")
def get_segmentation():
    data = load_analytics()
    return {
        "segment_scatter": data.get("segment_scatter", []),
        "segment_box": data.get("segment_box", [])
    }

@router.get("/ml-performance")
def get_ml_performance():
    data = load_analytics()
    return {
        "model_metrics": data.get("model_metrics", []),
        "roc_curves": data.get("roc_curves", {}),
        "pr_curves": data.get("pr_curves", {}),
        "confusion_matrix": data.get("confusion_matrix", []),
        "threshold_tradeoff": data.get("threshold_tradeoff", [])
    }

@router.get("/explainability")
def get_explainability():
    data = load_analytics()
    return {
        "shap_importance": data.get("shap_importance", [])
    }

@router.get("/risk-explorer")
def get_risk_explorer():
    data = load_analytics()
    return {
        "risk_distribution": data.get("risk_distribution", [])
    }
