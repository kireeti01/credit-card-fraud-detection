"""
Pydantic Schemas for FastAPI
============================
Defines request/response models for API validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FraudPrediction(str, Enum):
    """Fraud prediction enum."""
    FRAUD = "fraud"
    SAFE = "safe"


class TransactionInput(BaseModel):
    """
    Input schema for fraud prediction.
    Contains all 30 features from the credit card dataset.
    """
    time: float = Field(..., description="Seconds elapsed between this transaction and the first transaction", ge=0)
    v1: float = Field(..., description="PCA transformed feature V1")
    v2: float = Field(..., description="PCA transformed feature V2")
    v3: float = Field(..., description="PCA transformed feature V3")
    v4: float = Field(..., description="PCA transformed feature V4")
    v5: float = Field(..., description="PCA transformed feature V5")
    v6: float = Field(..., description="PCA transformed feature V6")
    v7: float = Field(..., description="PCA transformed feature V7")
    v8: float = Field(..., description="PCA transformed feature V8")
    v9: float = Field(..., description="PCA transformed feature V9")
    v10: float = Field(..., description="PCA transformed feature V10")
    v11: float = Field(..., description="PCA transformed feature V11")
    v12: float = Field(..., description="PCA transformed feature V12")
    v13: float = Field(..., description="PCA transformed feature V13")
    v14: float = Field(..., description="PCA transformed feature V14")
    v15: float = Field(..., description="PCA transformed feature V15")
    v16: float = Field(..., description="PCA transformed feature V16")
    v17: float = Field(..., description="PCA transformed feature V17")
    v18: float = Field(..., description="PCA transformed feature V18")
    v19: float = Field(..., description="PCA transformed feature V19")
    v20: float = Field(..., description="PCA transformed feature V20")
    v21: float = Field(..., description="PCA transformed feature V21")
    v22: float = Field(..., description="PCA transformed feature V22")
    v23: float = Field(..., description="PCA transformed feature V23")
    v24: float = Field(..., description="PCA transformed feature V24")
    v25: float = Field(..., description="PCA transformed feature V25")
    v26: float = Field(..., description="PCA transformed feature V26")
    v27: float = Field(..., description="PCA transformed feature V27")
    v28: float = Field(..., description="PCA transformed feature V28")
    amount: float = Field(..., description="Transaction amount", ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "time": 0.0,
                "v1": -1.3598071336738,
                "v2": -0.0727811733098497,
                "v3": 2.53634673796914,
                "v4": 1.37815522427443,
                "v5": -0.338320769942518,
                "v6": 0.462387777762292,
                "v7": 0.239598554061257,
                "v8": 0.0986979012610507,
                "v9": 0.363786969611213,
                "v10": 0.0907941719789316,
                "v11": -0.551599533260813,
                "v12": -0.617800855762348,
                "v13": -0.991389847235408,
                "v14": -0.311169353699879,
                "v15": 1.46817697209427,
                "v16": -0.470400525259478,
                "v17": 0.207971241929242,
                "v18": 0.0257905801985591,
                "v19": 0.403992960255733,
                "v20": 0.251412098239705,
                "v21": -0.018306777944153,
                "v22": 0.277837575558899,
                "v23": -0.110473910188767,
                "v24": 0.0669280749146731,
                "v25": 0.128539358273528,
                "v26": -0.189114843888824,
                "v27": 0.133558376740387,
                "v28": -0.0210530534538215,
                "amount": 149.62
            }
        }


class PredictionResponse(BaseModel):
    """
    Response schema for fraud prediction.
    """
    fraud: bool = Field(..., description="Whether the transaction is fraudulent")
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0, le=1)
    message: str = Field(..., description="Human-readable result message")
    transaction_id: Optional[str] = Field(None, description="Unique transaction ID")
    timestamp: Optional[str] = Field(None, description="Prediction timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "fraud": True,
                "confidence": 0.93,
                "message": "High risk transaction detected",
                "transaction_id": "txn_1234567890",
                "timestamp": "2026-02-08T12:34:56.789Z"
            }
        }


class TransactionLog(BaseModel):
    """
    Schema for transaction log stored in database.
    """
    transaction_id: str
    input_features: dict
    prediction: bool
    confidence: float
    timestamp: datetime
    client_ip: Optional[str] = None


class HealthResponse(BaseModel):
    """
    Health check response schema.
    """
    status: str
    model_loaded: bool
    scaler_loaded: bool
    database_connected: bool
    version: str


class BatchPredictionInput(BaseModel):
    """
    Input schema for batch predictions.
    """
    transactions: List[TransactionInput]


class BatchPredictionResponse(BaseModel):
    """
    Response schema for batch predictions.
    """
    predictions: List[PredictionResponse]
    total_processed: int
    fraud_count: int
    safe_count: int
