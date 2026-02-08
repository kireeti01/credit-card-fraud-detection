#!/bin/bash

# Credit Card Fraud Detection System - Setup Script
# =================================================

set -e

echo "🔥 Credit Card Fraud Detection System - Setup"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}$1${NC}"
    echo "----------------------------------------------"
}

# Check Python version
print_section "Checking Python version"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check Node.js version
print_section "Checking Node.js version"
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "Node.js version: $node_version"
else
    echo -e "${YELLOW}⚠️  Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

# Setup ML Environment
print_section "Setting up ML Environment"
cd ml

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing ML dependencies..."
pip install -q pandas numpy scikit-learn imbalanced-learn

echo "Generating synthetic data..."
python generate_synthetic_data.py

echo "Training ML models..."
python train_model.py

deactivate
cd ..

# Setup Backend
print_section "Setting up Backend"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -q -r requirements.txt

echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo ""
echo "To start the backend server, run:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"

deactivate
cd ..

# Setup Frontend
print_section "Setting up Frontend"
cd frontend

echo "Installing frontend dependencies..."
npm install --silent

echo -e "${GREEN}✅ Frontend setup complete!${NC}"
echo ""
echo "To start the frontend development server, run:"
echo "  cd frontend"
echo "  npm run dev"

cd ..

# Print summary
print_section "Setup Complete!"
echo -e "${GREEN}✅ All components installed successfully!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Start the Frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open your browser and navigate to:"
echo "   http://localhost:5173"
echo ""
echo "API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo -e "${GREEN}🚀 Happy fraud detecting!${NC}"
