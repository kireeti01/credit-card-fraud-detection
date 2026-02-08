"""
Database Module - MongoDB Integration
=====================================
Handles all database operations for storing prediction logs.
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, OperationFailure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    MongoDB database manager for fraud detection system.
    Handles connection, insertion, and retrieval of prediction logs.
    """
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.collection: Optional[Collection] = None
        self.is_connected = False
        
    def connect(self, connection_string: Optional[str] = None) -> bool:
        """
        Establish connection to MongoDB.
        
        Args:
            connection_string: MongoDB connection URI. If None, uses environment variable.
            
        Returns:
            True if connection successful, False otherwise.
        """
        try:
            # Get connection string
            mongo_uri = connection_string or os.getenv(
                'MONGODB_URI', 
                'mongodb://localhost:27017/'
            )
            
            logger.info(f"Connecting to MongoDB...")
            
            # Create client
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Verify connection
            self.client.admin.command('ping')
            
            # Setup database and collection
            self.db = self.client['fraud_detection']
            self.collection = self.db['prediction_logs']
            
            # Create indexes
            self._create_indexes()
            
            self.is_connected = True
            logger.info("✅ MongoDB connected successfully!")
            return True
            
        except ConnectionFailure as e:
            logger.warning(f"⚠️  MongoDB connection failed: {e}")
            logger.warning("Running in mock mode - predictions will not be persisted")
            self.is_connected = False
            return False
        except Exception as e:
            logger.error(f"❌ Database error: {e}")
            self.is_connected = False
            return False
    
    def _create_indexes(self) -> None:
        """Create necessary indexes for efficient queries."""
        if self.collection is not None:
            # Index on timestamp for sorting
            self.collection.create_index([("timestamp", DESCENDING)])
            # Index on prediction for filtering
            self.collection.create_index([("prediction", ASCENDING)])
            # Index on transaction_id for lookups
            self.collection.create_index([("transaction_id", ASCENDING)], unique=True)
            logger.info("✅ Database indexes created")
    
    def log_prediction(
        self, 
        transaction_id: str,
        input_features: Dict[str, Any],
        prediction: bool,
        confidence: float,
        client_ip: Optional[str] = None
    ) -> Optional[str]:
        """
        Log a prediction to the database.
        
        Args:
            transaction_id: Unique transaction identifier
            input_features: Input features used for prediction
            prediction: Fraud prediction result (True/False)
            confidence: Prediction confidence score
            client_ip: Client IP address
            
        Returns:
            Inserted document ID or None if failed.
        """
        if not self.is_connected or self.collection is None:
            logger.debug("Database not connected - skipping log")
            return None
        
        try:
            document = {
                "transaction_id": transaction_id,
                "input_features": input_features,
                "prediction": prediction,
                "confidence": confidence,
                "timestamp": datetime.utcnow(),
                "client_ip": client_ip
            }
            
            result = self.collection.insert_one(document)
            logger.debug(f"✅ Prediction logged: {transaction_id}")
            return str(result.inserted_id)
            
        except OperationFailure as e:
            logger.error(f"❌ Failed to log prediction: {e}")
            return None
    
    def get_recent_predictions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent prediction logs.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of prediction log documents.
        """
        if not self.is_connected or self.collection is None:
            return []
        
        try:
            cursor = self.collection.find().sort("timestamp", DESCENDING).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"❌ Failed to fetch predictions: {e}")
            return []
    
    def get_prediction_stats(self) -> Dict[str, Any]:
        """
        Get prediction statistics.
        
        Returns:
            Dictionary containing fraud/safe counts and other stats.
        """
        if not self.is_connected or self.collection is None:
            return {
                "total_predictions": 0,
                "fraud_count": 0,
                "safe_count": 0,
                "fraud_percentage": 0.0,
                "avg_confidence": 0.0
            }
        
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total": {"$sum": 1},
                        "fraud_count": {
                            "$sum": {"$cond": [{"$eq": ["$prediction", True]}, 1, 0]}
                        },
                        "safe_count": {
                            "$sum": {"$cond": [{"$eq": ["$prediction", False]}, 1, 0]}
                        },
                        "avg_confidence": {"$avg": "$confidence"}
                    }
                }
            ]
            
            result = list(self.collection.aggregate(pipeline))
            
            if result:
                stats = result[0]
                total = stats.get("total", 0)
                fraud_count = stats.get("fraud_count", 0)
                return {
                    "total_predictions": total,
                    "fraud_count": fraud_count,
                    "safe_count": stats.get("safe_count", 0),
                    "fraud_percentage": (fraud_count / total * 100) if total > 0 else 0.0,
                    "avg_confidence": stats.get("avg_confidence", 0.0)
                }
            
            return {
                "total_predictions": 0,
                "fraud_count": 0,
                "safe_count": 0,
                "fraud_percentage": 0.0,
                "avg_confidence": 0.0
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {
                "total_predictions": 0,
                "fraud_count": 0,
                "safe_count": 0,
                "fraud_percentage": 0.0,
                "avg_confidence": 0.0
            }
    
    def close(self) -> None:
        """Close database connection."""
        if self.client is not None:
            self.client.close()
            self.is_connected = False
            logger.info("🔌 MongoDB connection closed")


# Global database instance
db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    return db_manager
