#!/bin/bash
# Quick start script for documentation generation

set -e

echo "=================================================="
echo "Documentation Generator - Quick Start"
echo "=================================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.9+"
    exit 1
fi
echo "✓ Python: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found. Please install Node.js 20+"
    exit 1
fi
echo "✓ Node.js: $(node --version)"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Please install Docker"
    exit 1
fi
echo "✓ Docker: $(docker --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "✗ npm not found. Please install npm"
    exit 1
fi
echo "✓ npm: $(npm --version)"

echo ""

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo "✓ Python dependencies installed"
else
    source venv/bin/activate
    echo "✓ Using existing virtual environment"
fi

echo ""

# Check NIM endpoint
echo "Checking NVIDIA NIM endpoint..."
NIM_URL="${NIM_URL:-http://localhost:8000/v1}"

if curl -sf "$NIM_URL/models" > /dev/null 2>&1; then
    echo "✓ NIM endpoint is reachable at $NIM_URL"
    MODELS=$(curl -s "$NIM_URL/models" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', [])))")
    echo "  Found $MODELS model(s)"
else
    echo "⚠ NIM endpoint not reachable at $NIM_URL"
    echo "  Make sure NVIDIA NIM is running locally"
    echo "  Set NIM_URL environment variable if using a different endpoint"
fi

echo ""
echo "=================================================="
echo "Ready to generate documentation!"
echo "=================================================="
echo ""
echo "Usage:"
echo "  1. Create your spec file (see example-spec.json)"
echo "  2. Run: python generate_docs.py your-spec.json"
echo ""
echo "Quick test with example spec:"
echo "  python generate_docs.py example-spec.json --site-dir ./demo-docs"
echo ""
echo "For more options:"
echo "  python generate_docs.py --help"
echo ""
echo "See README.md and RUNBOOK.md for detailed documentation"
echo ""
