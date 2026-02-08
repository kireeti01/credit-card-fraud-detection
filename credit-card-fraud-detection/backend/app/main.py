"""
FastAPI Backend - Credit Card Fraud Detection API
=================================================
Main application entry point for the fraud detection REST API.

Endpoints:
- POST /predict: Single transaction fraud prediction
- POST /predict/batch: Batch prediction for multiple transactions
- GET /health: API health check
- GET /stats: Prediction statistics
- GET /recent: Recent predictions
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import local modules
from .schema import (
    TransactionInput, 
    PredictionResponse, 
    HealthResponse,
    BatchPredictionInput,
    BatchPredictionResponse
)
from .model import get_model
from .database import get_db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Version
API_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting up Fraud Detection API...")
    
    # Load ML model
    model = get_model()
    model.load_model()
    model.load_scaler()
    
    # Connect to database
    db = get_db_manager()
    db.connect()
    
    logger.info("✅ Startup complete!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    db.close()
    logger.info("✅ Shutdown complete!")


# Create FastAPI app
app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="""
    Production-ready API for detecting fraudulent credit card transactions using Machine Learning.
    
    ## Features
    - **Single Prediction**: Check if a single transaction is fraudulent
    - **Batch Prediction**: Process multiple transactions at once
    - **Real-time**: Fast inference with sub-100ms response time
    - **Logging**: All predictions are logged for analytics
    
    ## Models
    - Random Forest classifier trained on credit card transaction data
    - SMOTE applied for handling class imbalance
    - StandardScaler for feature normalization
    """,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Credit Card Fraud Detection API",
        "version": API_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API and its dependencies.
    """
    model = get_model()
    db = get_db_manager()
    
    return HealthResponse(
        status="healthy",
        model_loaded=model.model_loaded,
        scaler_loaded=model.scaler_loaded,
        database_connected=db.is_connected,
        version=API_VERSION
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful prediction"},
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"}
    }
)
async def predict_fraud(
    transaction: TransactionInput,
    request: Request
):
    """
    Predict if a credit card transaction is fraudulent.
    
    This endpoint accepts transaction features and returns a fraud prediction
    with confidence score.
    
    ## Input
    - All 30 features from the credit card dataset (Time, V1-V28, Amount)
    
    ## Output
    - **fraud**: Boolean indicating if transaction is fraudulent
    - **confidence**: Probability score (0-1)
    - **message**: Human-readable result message
    - **transaction_id**: Unique identifier for this prediction
    """
    try:
        model = get_model()
        db = get_db_manager()
        
        # Validate model is loaded
        if not model.model_loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded"
            )
        
        # Generate transaction ID
        transaction_id = f"txn_{uuid.uuid4().hex[:16]}"
        
        # Convert input to dict
        features = transaction.model_dump()
        
        # Make prediction
        is_fraud, confidence, message = model.predict(features)
        
        # Log to database
        client_ip = request.client.host if request.client else None
        db.log_prediction(
            transaction_id=transaction_id,
            input_features=features,
            prediction=is_fraud,
            confidence=confidence,
            client_ip=client_ip
        )
        
        logger.info(f"Prediction: {transaction_id} - Fraud: {is_fraud}, Confidence: {confidence:.4f}")
        
        return PredictionResponse(
            fraud=is_fraud,
            confidence=confidence,
            message=message,
            transaction_id=transaction_id,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    tags=["Prediction"],
    status_code=status.HTTP_200_OK
)
async def predict_batch(
    batch: BatchPredictionInput,
    request: Request
):
    """
    Predict fraud for multiple transactions in a single request.
    
    ## Input
    - List of transaction objects (max 100 per request)
    
    ## Output
    - List of predictions for each transaction
    - Summary statistics (total, fraud count, safe count)
    """
    try:
        model = get_model()
        db = get_db_manager()
        
        # Validate model is loaded
        if not model.model_loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded"
            )
        
        # Limit batch size
        if len(batch.transactions) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size exceeds maximum of 100 transactions"
            )
        
        predictions = []
        fraud_count = 0
        client_ip = request.client.host if request.client else None
        
        for transaction in batch.transactions:
            # Generate transaction ID
            transaction_id = f"txn_{uuid.uuid4().hex[:16]}"
            
            # Convert input to dict
            features = transaction.model_dump()
            
            # Make prediction
            is_fraud, confidence, message = model.predict(features)
            
            if is_fraud:
                fraud_count += 1
            
            # Log to database
            db.log_prediction(
                transaction_id=transaction_id,
                input_features=features,
                prediction=is_fraud,
                confidence=confidence,
                client_ip=client_ip
            )
            
            predictions.append(PredictionResponse(
                fraud=is_fraud,
                confidence=confidence,
                message=message,
                transaction_id=transaction_id,
                timestamp=datetime.utcnow().isoformat()
            ))
        
        logger.info(f"Batch prediction: {len(predictions)} transactions, {fraud_count} fraud detected")
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_processed=len(predictions),
            fraud_count=fraud_count,
            safe_count=len(predictions) - fraud_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/stats", tags=["Analytics"])
async def get_stats():
    """
    Get prediction statistics.
    
    Returns aggregated statistics about predictions made.
    """
    try:
        db = get_db_manager()
        stats = db.get_prediction_stats()
        
        return {
            "status": "success",
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@app.get("/recent", tags=["Analytics"])
async def get_recent_predictions(limit: int = 10):
    """
    Get recent prediction logs.
    
    ## Parameters
    - **limit**: Number of recent predictions to return (default: 10, max: 100)
    
    ## Output
    - List of recent prediction records
    """
    try:
        # Validate limit
        if limit < 1 or limit > 100:
            limit = 10
        
        db = get_db_manager()
        predictions = db.get_recent_predictions(limit=limit)
        
        # Convert ObjectId to string for JSON serialization
        for pred in predictions:
            pred['_id'] = str(pred['_id'])
            pred['timestamp'] = pred['timestamp'].isoformat() if 'timestamp' in pred else None
        
        return {
            "status": "success",
            "count": len(predictions),
            "data": predictions
        }
        
    except Exception as e:
        logger.error(f"Recent predictions error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recent predictions: {str(e)}"
        )


@app.get("/model/info", tags=["Model"])
async def get_model_info():
    """
    Get information about the loaded ML model.
    
    Returns model metadata and feature information.
    """
    model = get_model()
    return {
        "status": "success",
        "data": model.get_model_info()
    }


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
