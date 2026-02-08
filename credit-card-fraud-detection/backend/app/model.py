"""
ML Model Module
===============
Handles loading and inference with the trained fraud detection model.
"""

import os
import pickle
import logging
import numpy as np
from typing import Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FraudDetectionModel:
    """
    Fraud Detection Model wrapper.
    Loads and performs inference with the trained Random Forest model.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self.scaler_loaded = False
        self.feature_names = [
            'Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9',
            'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19',
            'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount'
        ]
        
    def load_model(self, model_path: Optional[str] = None) -> bool:
        """
        Load the trained model from disk.
        
        Args:
            model_path: Path to the model pickle file. If None, uses default path.
            
        Returns:
            True if model loaded successfully, False otherwise.
        """
        try:
            # Determine model path
            if model_path is None:
                # Get the directory of this file
                current_dir = os.path.dirname(os.path.abspath(__file__))
                model_path = os.path.join(current_dir, '..', 'model', 'fraud_model.pkl')
            
            model_path = os.path.abspath(model_path)
            logger.info(f"Loading model from: {model_path}")
            
            if not os.path.exists(model_path):
                logger.error(f"❌ Model file not found: {model_path}")
                return False
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            self.model_loaded = True
            logger.info("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.model_loaded = False
            return False
    
    def load_scaler(self, scaler_path: Optional[str] = None) -> bool:
        """
        Load the feature scaler from disk.
        
        Args:
            scaler_path: Path to the scaler pickle file. If None, uses default path.
            
        Returns:
            True if scaler loaded successfully, False otherwise.
        """
        try:
            # Determine scaler path
            if scaler_path is None:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                scaler_path = os.path.join(current_dir, '..', 'model', 'scaler.pkl')
            
            scaler_path = os.path.abspath(scaler_path)
            logger.info(f"Loading scaler from: {scaler_path}")
            
            if not os.path.exists(scaler_path):
                logger.error(f"❌ Scaler file not found: {scaler_path}")
                return False
            
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            self.scaler_loaded = True
            logger.info("✅ Scaler loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load scaler: {e}")
            self.scaler_loaded = False
            return False
    
    def predict(self, features: dict) -> Tuple[bool, float, str]:
        """
        Make a fraud prediction on input features.
        
        Args:
            features: Dictionary containing transaction features
            
        Returns:
            Tuple of (is_fraud, confidence, message)
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Extract features in correct order
            feature_array = self._extract_features(features)
            
            # Apply scaling if scaler is available
            if self.scaler_loaded and self.scaler is not None:
                feature_array = self._apply_scaling(feature_array)
            
            # Reshape for single prediction
            X = feature_array.reshape(1, -1)
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            confidence = self.model.predict_proba(X)[0][1]  # Probability of fraud class
            
            # Determine message based on confidence
            is_fraud = bool(prediction == 1)
            message = self._get_message(is_fraud, confidence)
            
            return is_fraud, float(confidence), message
            
        except Exception as e:
            logger.error(f"❌ Prediction error: {e}")
            raise
    
    def _extract_features(self, features: dict) -> np.ndarray:
        """
        Extract features from input dictionary in correct order.
        
        Args:
            features: Input feature dictionary
            
        Returns:
            NumPy array of features
        """
        # Map input keys to feature names
        feature_map = {
            'time': 'Time',
            'v1': 'V1', 'v2': 'V2', 'v3': 'V3', 'v4': 'V4',
            'v5': 'V5', 'v6': 'V6', 'v7': 'V7', 'v8': 'V8', 'v9': 'V9',
            'v10': 'V10', 'v11': 'V11', 'v12': 'V12', 'v13': 'V13', 'v14': 'V14',
            'v15': 'V15', 'v16': 'V16', 'v17': 'V17', 'v18': 'V18', 'v19': 'V19',
            'v20': 'V20', 'v21': 'V21', 'v22': 'V22', 'v23': 'V23', 'v24': 'V24',
            'v25': 'V25', 'v26': 'V26', 'v27': 'V27', 'v28': 'V28',
            'amount': 'Amount'
        }
        
        # Build feature array
        feature_array = []
        for key, feature_name in feature_map.items():
            value = features.get(key, 0.0)
            feature_array.append(float(value))
        
        return np.array(feature_array)
    
    def _apply_scaling(self, feature_array: np.ndarray) -> np.ndarray:
        """
        Apply scaling to Time and Amount features.
        
        Args:
            feature_array: Raw feature array
            
        Returns:
            Scaled feature array
        """
        # Create a copy to avoid modifying original
        scaled = feature_array.copy()
        
        # Time is at index 0, Amount is at index 29
        time_amount = scaled[[0, 29]].reshape(1, -1)
        scaled_time_amount = self.scaler.transform(time_amount)
        
        scaled[0] = scaled_time_amount[0, 0]
        scaled[29] = scaled_time_amount[0, 1]
        
        return scaled
    
    def _get_message(self, is_fraud: bool, confidence: float) -> str:
        """
        Generate human-readable message based on prediction.
        
        Args:
            is_fraud: Whether fraud was detected
            confidence: Prediction confidence
            
        Returns:
            Human-readable message
        """
        if is_fraud:
            if confidence > 0.9:
                return "🚨 High risk transaction detected! Immediate attention required."
            elif confidence > 0.7:
                return "⚠️  Suspicious transaction detected. Review recommended."
            else:
                return "⚡ Potential fraud detected. Please verify."
        else:
            if confidence < 0.1:
                return "✅ Transaction appears safe."
            elif confidence < 0.3:
                return "✅ Low risk transaction."
            else:
                return "✅ Transaction within normal parameters."
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_loaded": self.model_loaded,
            "scaler_loaded": self.scaler_loaded,
            "feature_count": len(self.feature_names),
            "features": self.feature_names
        }


# Global model instance
fraud_model = FraudDetectionModel()


def get_model() -> FraudDetectionModel:
    """Get the global fraud detection model instance."""
    return fraud_model
