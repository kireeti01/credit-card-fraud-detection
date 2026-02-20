from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(
    title="Credit Card Fraud Detection API",
    version="1.0.0"
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# In-memory storage
# -------------------------
stats = {
    "total_predictions": 0,
    "fraud_count": 0,
    "safe_count": 0
}

transactions = []

# -------------------------
# Request model
# -------------------------
class Transaction(BaseModel):
    time: float
    amount: float
    v1: float
    v2: float
    v3: float
    v4: float
    v5: float
    v6: float
    v7: float
    v8: float
    v9: float
    v10: float
    v11: float
    v12: float
    v13: float
    v14: float
    v15: float
    v16: float
    v17: float
    v18: float
    v19: float
    v20: float
    v21: float
    v22: float
    v23: float
    v24: float
    v25: float
    v26: float
    v27: float
    v28: float

# -------------------------
# Root
# -------------------------
@app.get("/")
def root():
    return {
        "name": "Credit Card Fraud Detection API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Stats
# -------------------------
@app.get("/stats")
def get_stats():
    fraud_percentage = (
        (stats["fraud_count"] / stats["total_predictions"]) * 100
        if stats["total_predictions"] > 0
        else 0
    )

    return {
        "data": {
            "total_predictions": stats["total_predictions"],
            "fraud_count": stats["fraud_count"],
            "safe_count": stats["safe_count"],
            "fraud_percentage": round(fraud_percentage, 2)
        }
    }

# -------------------------
# Prediction
# -------------------------
@app.post("/predict")
def predict(transaction: Transaction):
    fraud_probability = random.random()
    is_fraud = fraud_probability > 0.7

    stats["total_predictions"] += 1
    if is_fraud:
        stats["fraud_count"] += 1
    else:
        stats["safe_count"] += 1

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "amount": transaction.amount,
        "is_fraud": is_fraud,
        "fraud_probability": round(fraud_probability, 3)
    }

    transactions.append(record)

    return {
        "is_fraud": is_fraud,
        "fraud_probability": round(fraud_probability, 3),
        "message": "Fraud detected" if is_fraud else "Transaction is safe"
    }

# -------------------------
# Recent transactions (FIX)
# -------------------------
@app.get("/recent")
def get_recent(limit: int = 50):
    return {
        "data": transactions[-limit:][::-1]
    }
