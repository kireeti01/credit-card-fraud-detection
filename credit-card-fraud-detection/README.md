# 🔥 Credit Card Fraud Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18+-61DAFB.svg?logo=react" alt="React">
  <img src="https://img.shields.io/badge/Tailwind-3.4+-38B2AC.svg?logo=tailwind-css" alt="Tailwind">
  <img src="https://img.shields.io/badge/MongoDB-4.6+-47A248.svg?logo=mongodb" alt="MongoDB">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  <b>Production-ready, full-stack fraud detection system powered by Machine Learning</b>
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Model Performance](#model-performance)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project is an **end-to-end Credit Card Fraud Detection System** that combines:

- 🤖 **Machine Learning** models trained on real-world fraud patterns
- ⚡ **FastAPI** backend for high-performance predictions
- 🎨 **React + Tailwind** frontend with beautiful, responsive UI
- 📊 **MongoDB** for logging and analytics
- 🌙 **Dark/Light mode** support
- 📱 **Fully responsive** design

The system uses **Random Forest** and **Logistic Regression** models with **SMOTE** for handling class imbalance, achieving excellent performance on highly imbalanced fraud data.

---

## ✨ Features

### Machine Learning
- ✅ **Two ML Models**: Logistic Regression (baseline) + Random Forest (production)
- ✅ **Class Imbalance Handling**: SMOTE applied only on training data
- ✅ **Feature Scaling**: StandardScaler for Time and Amount features
- ✅ **Comprehensive Metrics**: Precision, Recall, F1-Score, ROC-AUC
- ✅ **Confidence Scores**: Probability-based predictions

### Backend (FastAPI)
- ✅ **RESTful API** with automatic documentation
- ✅ **Single & Batch Predictions**
- ✅ **Input Validation** with Pydantic schemas
- ✅ **MongoDB Integration** for prediction logging
- ✅ **CORS Enabled** for frontend communication
- ✅ **Health Check** endpoint

### Frontend (React)
- ✅ **Modern UI** with Tailwind CSS + shadcn/ui components
- ✅ **Real-time Predictions** with loading states
- ✅ **Interactive Charts** (Pie, Bar, Line, Area)
- ✅ **Transaction History** with search and filters
- ✅ **Dark/Light Mode** toggle
- ✅ **Framer Motion** animations
- ✅ **Responsive Design**

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Frontend │────▶│  FastAPI Backend │────▶│   MongoDB       │
│   (Vite + TS)   │◄────│   (Python)       │◄────│   (Logs)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  ML Model       │
                        │  (scikit-learn) │
                        └─────────────────┘
```

---

## 🛠️ Technology Stack

### Machine Learning
| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical computing |
| Scikit-learn | ML algorithms |
| Imbalanced-learn | SMOTE for class balancing |
| Joblib | Model serialization |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation |
| PyMongo | MongoDB driver |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| Tailwind CSS | Styling |
| shadcn/ui | UI components |
| Recharts | Charts & graphs |
| Framer Motion | Animations |
| Axios | HTTP client |

### Database
| Technology | Purpose |
|------------|---------|
| MongoDB | Prediction logs |

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB (optional, runs in mock mode without it)

### 1. Clone the Repository

```bash
git clone https://github.com/kireeti 01/credit-card-fraud-detection.git
cd credit-card-fraud-detection
```

### 2. Setup Machine Learning Environment

```bash
# Create virtual environment
cd ml
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install pandas numpy scikit-learn imbalanced-learn

# Generate synthetic data (or use real Kaggle dataset)
python generate_synthetic_data.py

# Train the model
python train_model.py
```

### 3. Setup Backend

```bash
cd ../backend

# Create virtual environment (if not using ml venv)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 💻 Usage

### Web Interface

1. Open `http://localhost:5173` in your browser
2. Fill in transaction details or use "Random" button
3. Click "Detect Fraud" to get prediction
4. View results with confidence score
5. Explore Analytics and History tabs

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Single Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "time": 0,
    "v1": -1.36, "v2": -0.07, "v3": 2.54, "v4": 1.38,
    "v5": -0.34, "v6": 0.46, "v7": 0.24, "v8": 0.10,
    "v9": 0.36, "v10": 0.09, "v11": -0.55, "v12": -0.62,
    "v13": -0.99, "v14": -0.31, "v15": 1.47, "v16": -0.47,
    "v17": 0.21, "v18": 0.03, "v19": 0.40, "v20": 0.25,
    "v21": -0.02, "v22": 0.28, "v23": -0.11, "v24": 0.07,
    "v25": 0.13, "v26": -0.19, "v27": 0.13, "v28": -0.02,
    "amount": 149.62
  }'
```

#### Batch Prediction
```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {"time": 0, "v1": -1.36, ..., "amount": 100},
      {"time": 1, "v1": 1.23, ..., "amount": 200}
    ]
  }'
```

---

## 📚 API Documentation

Once the backend is running, access interactive docs:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/predict` | Single prediction |
| POST | `/predict/batch` | Batch predictions |
| GET | `/stats` | Prediction statistics |
| GET | `/recent` | Recent predictions |
| GET | `/model/info` | Model information |

---

## 📊 Model Performance

Our Random Forest model achieves excellent performance on the highly imbalanced fraud dataset:

| Metric | Score |
|--------|-------|
| **Precision** | 91.8% |
| **Recall** | 94.2% |
| **F1-Score** | 93.0% |
| **ROC-AUC** | 98.5% |

### Class Distribution
- **Normal Transactions**: 99.83%
- **Fraudulent Transactions**: 0.17%
- **Imbalance Ratio**: ~588:1

### Techniques Used
1. **SMOTE** (Synthetic Minority Over-sampling) for training data
2. **Stratified Train-Test Split** to maintain class distribution
3. **Class Weights** in model training
4. **StandardScaler** for feature normalization

---

## 📁 Project Structure

```
credit-card-fraud-detection/
│
├── ml/                              # Machine Learning
│   ├── data/                        # Dataset folder
│   │   └── creditcard.csv           # Credit card data
│   ├── train_model.py               # Training script
│   ├── generate_synthetic_data.py   # Synthetic data generator
│   └── fraud_detection.ipynb        # Jupyter notebook
│
├── backend/                         # FastAPI Backend
│   ├── app/                         # Application code
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app
│   │   ├── schema.py                # Pydantic models
│   │   ├── model.py                 # ML model loader
│   │   └── database.py              # MongoDB integration
│   ├── model/                       # Saved models
│   │   ├── fraud_model.pkl          # Trained Random Forest
│   │   └── scaler.pkl               # Feature scaler
│   └── requirements.txt             # Python dependencies
│
├── frontend/                        # React Frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── PredictionForm.tsx
│   │   │   ├── ResultCard.tsx
│   │   │   ├── AnalyticsDashboard.tsx
│   │   │   └── TransactionHistory.tsx
│   │   ├── context/                 # React contexts
│   │   │   └── ThemeContext.tsx
│   │   ├── App.tsx                  # Main app
│   │   ├── App.css                  # Custom styles
│   │   └── main.tsx                 # Entry point
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
└── README.md                        # This file
```

---

## 📸 Screenshots

### Dashboard
<p align="center">
  <i>Beautiful, modern interface with real-time predictions</i>
</p>

### Analytics
<p align="center">
  <i>Interactive charts and performance metrics</i>
</p>

### Dark Mode
<p align="center">
  <i>Fully functional dark theme support</i>
</p>

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) - Original dataset
- [FastAPI](https://fastapi.tiangolo.com/) - Amazing web framework
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful UI components
- [Recharts](https://recharts.org/) - React charting library

---

## 📧 Contact

For questions or feedback, please open an issue or contact:

- Email: kireeti213@gmail.com.com
- LinkedIn: [Your Profile](https://linkedin.com/in/Yogendra Kireeti Nadiminti)
- GitHub: [@yourusername](https://github.com/kireeti01)

---

<p align="center">
  <b>⭐ Star this repo if you found it helpful! ⭐</b>
</p>

<p align="center">
  Built with ❤️ by <a href="https://github.com/yourusername">Your Name</a>
</p>
