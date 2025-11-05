#!/bin/bash

# Setup script for Docker Sandbox feature
# This script builds the Docker image and verifies the setup

set -e  # Exit on error

echo "========================================="
echo "OptimizeHub Docker Sandbox Setup"
echo "========================================="
echo ""

# Check if Docker is installed
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed or not in PATH"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker is installed: $(docker --version)"
echo ""

# Check if Docker daemon is running
echo "Checking if Docker daemon is running..."
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker daemon is not running"
    echo "Please start Docker Desktop (Mac/Windows) or Docker service (Linux)"
    exit 1
fi

echo "✅ Docker daemon is running"
echo ""

# Navigate to backend directory
echo "Navigating to backend directory..."
cd "$(dirname "$0")/backend"
echo "✅ Current directory: $(pwd)"
echo ""

# Check if Dockerfile exists
echo "Checking if Dockerfile exists..."
if [ ! -f "docker/Dockerfile.sandbox" ]; then
    echo "❌ Error: Dockerfile not found at docker/Dockerfile.sandbox"
    exit 1
fi

echo "✅ Dockerfile found"
echo ""

# Build Docker image
echo "Building Docker sandbox image..."
echo "This may take a few minutes on first run..."
echo ""

if docker build -t optimizehub-sandbox:latest -f docker/Dockerfile.sandbox docker/; then
    echo ""
    echo "✅ Docker image built successfully!"
else
    echo ""
    echo "❌ Error: Failed to build Docker image"
    exit 1
fi

echo ""

# Verify image was created
echo "Verifying Docker image..."
if docker images optimizehub-sandbox:latest | grep -q optimizehub-sandbox; then
    echo "✅ Docker image verified"
    echo ""
    docker images optimizehub-sandbox:latest
else
    echo "❌ Error: Docker image not found after build"
    exit 1
fi

echo ""
echo "========================================="
echo "Setup Complete! ✨"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Install backend dependencies:"
echo "   cd backend && pip install -r requirements.txt"
echo ""
echo "2. Start the backend server:"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "3. Start the frontend (in another terminal):"
echo "   cd frontend && npm install && npm run dev"
echo ""
echo "4. Test with example files:"
echo "   curl -X POST http://localhost:8000/api/optimize/custom \\"
echo "     -F \"fitness_file=@examples/custom_fitness/sphere_fitness.py\" \\"
echo "     -F \"config_file=@examples/custom_fitness/sphere_config.yaml\""
echo ""
echo "For detailed instructions, see: DOCKER_SANDBOX_SETUP.md"
echo ""
