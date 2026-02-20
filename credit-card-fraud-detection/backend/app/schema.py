"""
Pydantic Schemas for FastAPI
============================
Request/response validation models.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FraudPrediction(str, Enum):
    FRAUD = "fraud"
    SAFE = "safe"


class TransactionInput(BaseModel):
    time: float = Field(default=0.0, ge=0)
    v1: float = 0.0
    v2: float = 0.0
    v3: float = 0.0
    v4: float = 0.0
    v5: float = 0.0
    v6: float = 0.0
    v7: float = 0.0
    v8: float = 0.0
    v9: float = 0.0
    v10: float = 0.0
    v11: float = 0.0
    v12: float = 0.0
    v13: float = 0.0
    v14: float = 0.0
    v15: float = 0.0
    v16: float = 0.0
    v17: float = 0.0
    v18: float = 0.0
    v19: float = 0.0
    v20: float = 0.0
    v21: float = 0.0
    v22: float = 0.0
    v23: float = 0.0
    v24: float = 0.0
    v25: float = 0.0
    v26: float = 0.0
    v27: float = 0.0
    v28: float = 0.0
    amount: float = Field(default=0.0, ge=0)

    @field_validator("*", mode="before")
    @classmethod
    def convert_empty_to_zero(cls, v):
        if v in ("", None):
            return 0.0
        return float(v)


class PredictionResponse(BaseModel):
    fraud: bool
    confidence: float = Field(ge=0, le=1)
    message: str
    transaction_id: Optional[str] = None
    timestamp: Optional[str] = None


class TransactionLog(BaseModel):
    transaction_id: str
    input_features: dict
    prediction: bool
    confidence: float
    timestamp: datetime
    client_ip: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    scaler_loaded: bool
    database_connected: bool
    version: str


class BatchPredictionInput(BaseModel):
    transactions: List[TransactionInput]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_processed: int
    fraud_count: int
    safe_count: int
