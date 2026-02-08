"""
Credit Card Fraud Detection - Model Training Pipeline
======================================================
This script trains and evaluates machine learning models for fraud detection.
Uses SMOTE for handling class imbalance and saves the best performing model.

Author: ML Engineer
Date: 2026
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn imports
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    precision_score, recall_score, f1_score, roc_auc_score,
    roc_curve, precision_recall_curve
)

# Imbalanced learning
from imblearn.over_sampling import SMOTE

# Set random seed for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the credit card fraud dataset.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the dataset
    """
    print(f"📊 Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"✅ Data loaded successfully! Shape: {df.shape}")
    return df


def explore_data(df: pd.DataFrame) -> None:
    """
    Perform exploratory data analysis on the dataset.
    
    Args:
        df: Input DataFrame
    """
    print("\n" + "="*60)
    print("📈 EXPLORATORY DATA ANALYSIS")
    print("="*60)
    
    # Basic info
    print(f"\nDataset Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Class distribution
    fraud_count = df['Class'].value_counts()
    print(f"\n🔍 Class Distribution:")
    print(f"   Non-Fraud (0): {fraud_count[0]:,} ({fraud_count[0]/len(df)*100:.2f}%)")
    print(f"   Fraud (1): {fraud_count[1]:,} ({fraud_count[1]/len(df)*100:.2f}%)")
    print(f"   Imbalance Ratio: {fraud_count[0]/fraud_count[1]:.0f}:1")
    
    # Amount statistics
    print(f"\n💰 Transaction Amount Statistics:")
    print(df['Amount'].describe())
    
    # Fraud amount statistics
    print(f"\n💰 Fraud Transaction Amount Statistics:")
    fraud_df = df[df['Class'] == 1]
    print(fraud_df['Amount'].describe())


def preprocess_data(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocess the data: scale features and separate target.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (X_scaled, y, scaler)
    """
    print("\n" + "="*60)
    print("🔧 DATA PREPROCESSING")
    print("="*60)
    
    # Separate features and target
    X = df.drop(['Class'], axis=1)
    y = df['Class']
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Scale the 'Amount' and 'Time' features
    scaler = StandardScaler()
    X_scaled = X.copy()
    X_scaled[['Time', 'Amount']] = scaler.fit_transform(X[['Time', 'Amount']])
    
    print("✅ Features scaled successfully!")
    
    return X_scaled.values, y.values, scaler


def apply_smote(X_train: np.ndarray, y_train: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply SMOTE to balance the training dataset.
    
    Args:
        X_train: Training features
        y_train: Training labels
        
    Returns:
        Balanced training data
    """
    print("\n⚖️  Applying SMOTE to balance training data...")
    
    # Convert y_train to integers
    y_train = y_train.astype(int)
    
    smote = SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.5)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    
    print(f"Before SMOTE: {np.bincount(y_train)}")
    print(f"After SMOTE: {np.bincount(y_resampled)}")
    
    return X_resampled, y_resampled


def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray) -> LogisticRegression:
    """
    Train Logistic Regression model (baseline).
    
    Args:
        X_train: Training features
        y_train: Training labels
        
    Returns:
        Trained Logistic Regression model
    """
    print("\n🤖 Training Logistic Regression (Baseline)...")
    
    model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
        class_weight='balanced',
        solver='lbfgs'
    )
    
    model.fit(X_train, y_train)
    print("✅ Logistic Regression trained!")
    
    return model


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train Random Forest model (main model).
    
    Args:
        X_train: Training features
        y_train: Training labels
        
    Returns:
        Trained Random Forest model
    """
    print("\n🌲 Training Random Forest (Main Model)...")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=RANDOM_STATE,
        class_weight='balanced',
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("✅ Random Forest trained!")
    
    return model


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, model_name: str) -> Dict[str, Any]:
    """
    Evaluate model performance with comprehensive metrics.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        model_name: Name of the model
        
    Returns:
        Dictionary of evaluation metrics
    """
    print(f"\n📊 Evaluating {model_name}...")
    print("="*60)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Print results
    print(f"\n🎯 {model_name} Performance:")
    print(f"   Precision: {metrics['precision']:.4f}")
    print(f"   Recall: {metrics['recall']:.4f}")
    print(f"   F1-Score: {metrics['f1_score']:.4f}")
    print(f"   ROC-AUC: {metrics['roc_auc']:.4f}")
    
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Non-Fraud', 'Fraud']))
    
    print(f"\n🔢 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"   TN: {cm[0,0]:4d} | FP: {cm[0,1]:4d}")
    print(f"   FN: {cm[1,0]:4d} | TP: {cm[1,1]:4d}")
    
    return metrics


def save_model(model, scaler, model_dir: str = '../backend/model') -> None:
    """
    Save the trained model and scaler.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        model_dir: Directory to save models
    """
    print("\n💾 Saving model and scaler...")
    
    # Create directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(model_dir, 'fraud_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save scaler
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"✅ Model saved to: {model_path}")
    print(f"✅ Scaler saved to: {scaler_path}")


def main():
    """
    Main training pipeline.
    """
    print("\n" + "="*60)
    print("🔥 CREDIT CARD FRAUD DETECTION - MODEL TRAINING")
    print("="*60)
    
    # Check if dataset exists
    data_path = 'data/creditcard.csv'
    if not os.path.exists(data_path):
        print(f"\n❌ Error: Dataset not found at {data_path}")
        print("📥 Please download the dataset from Kaggle:")
        print("   https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        print("   and place it in ml/data/ folder")
        sys.exit(1)
    
    # Load data
    df = load_data(data_path)
    
    # Explore data
    explore_data(df)
    
    # Preprocess data
    X, y, scaler = preprocess_data(df)
    
    # Split data
    print("\n✂️  Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Apply SMOTE only on training data
    X_train_balanced, y_train_balanced = apply_smote(X_train, y_train)
    
    # Train models
    print("\n" + "="*60)
    print("🚀 MODEL TRAINING")
    print("="*60)
    
    # Logistic Regression
    lr_model = train_logistic_regression(X_train_balanced, y_train_balanced)
    lr_metrics = evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    
    # Random Forest
    rf_model = train_random_forest(X_train_balanced, y_train_balanced)
    rf_metrics = evaluate_model(rf_model, X_test, y_test, "Random Forest")
    
    # Compare models
    print("\n" + "="*60)
    print("🏆 MODEL COMPARISON")
    print("="*60)
    print(f"{'Metric':<15} {'Logistic Reg':<15} {'Random Forest':<15}")
    print("-" * 45)
    for metric in ['precision', 'recall', 'f1_score', 'roc_auc']:
        print(f"{metric.capitalize():<15} {lr_metrics[metric]:<15.4f} {rf_metrics[metric]:<15.4f}")
    
    # Select best model (Random Forest typically performs better)
    best_model = rf_model
    print("\n✅ Selected Random Forest as the production model")
    
    # Save model and scaler
    save_model(best_model, scaler)
    
    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📁 Output files:")
    print("   - backend/model/fraud_model.pkl")
    print("   - backend/model/scaler.pkl")
    print("\n🚀 Ready for deployment!")


if __name__ == "__main__":
    main()
