"""
Synthetic Credit Card Fraud Data Generator
==========================================
Generates realistic synthetic data that mimics the Kaggle Credit Card Fraud Dataset.
Use this when the actual dataset is not available.

The synthetic data maintains:
- Similar feature distributions (PCA-transformed features V1-V28)
- Time and Amount features
- Severe class imbalance (~0.17% fraud)
"""

import numpy as np
import pandas as pd
import os

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


def generate_synthetic_data(n_samples: int = 284807, fraud_ratio: float = 0.0017) -> pd.DataFrame:
    """
    Generate synthetic credit card transaction data.
    
    Args:
        n_samples: Total number of transactions (default: same as original dataset)
        fraud_ratio: Ratio of fraudulent transactions (default: 0.17%)
        
    Returns:
        DataFrame with synthetic transaction data
    """
    print(f"🎲 Generating {n_samples:,} synthetic transactions...")
    
    n_fraud = int(n_samples * fraud_ratio)
    n_normal = n_samples - n_fraud
    
    # Generate Time feature (seconds since first transaction)
    time_normal = np.random.exponential(100, n_normal)
    time_normal = np.cumsum(time_normal)
    time_normal = time_normal / time_normal.max() * 172792  # Scale to match original
    
    time_fraud = np.random.uniform(0, 172792, n_fraud)
    
    # Generate Amount feature
    amount_normal = np.random.lognormal(4, 1.5, n_normal)
    amount_fraud = np.random.lognormal(5, 1.2, n_fraud)
    
    # Generate V1-V28 features (PCA components)
    # Normal transactions cluster around origin
    v_features_normal = np.random.multivariate_normal(
        mean=np.zeros(28),
        cov=np.eye(28) * 0.5,
        size=n_normal
    )
    
    # Fraud transactions have different patterns
    fraud_mean = np.random.normal(0, 1.5, 28)
    v_features_fraud = np.random.multivariate_normal(
        mean=fraud_mean,
        cov=np.eye(28) * 2,
        size=n_fraud
    )
    
    # Combine data
    X_normal = np.column_stack([time_normal, v_features_normal, amount_normal])
    X_fraud = np.column_stack([time_fraud, v_features_fraud, amount_fraud])
    
    # Create labels
    y_normal = np.zeros(n_normal)
    y_fraud = np.ones(n_fraud)
    
    # Combine and shuffle
    X = np.vstack([X_normal, X_fraud])
    y = np.hstack([y_normal, y_fraud])
    
    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]
    
    # Create DataFrame
    columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount', 'Class']
    data = np.column_stack([X, y])
    df = pd.DataFrame(data, columns=columns)
    
    print(f"✅ Generated {n_samples:,} transactions")
    print(f"   Normal: {n_normal:,} ({(n_normal/n_samples)*100:.2f}%)")
    print(f"   Fraud: {n_fraud:,} ({(n_fraud/n_samples)*100:.2f}%)")
    
    return df


def main():
    """Generate and save synthetic dataset."""
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate data
    df = generate_synthetic_data(n_samples=50000)  # Smaller for faster training
    
    # Save to CSV
    output_path = 'data/creditcard.csv'
    df.to_csv(output_path, index=False)
    print(f"\n💾 Data saved to: {output_path}")
    
    # Display statistics
    print("\n📊 Dataset Statistics:")
    print(df.describe())
    
    print("\n🔍 Class Distribution:")
    print(df['Class'].value_counts())


if __name__ == "__main__":
    main()
