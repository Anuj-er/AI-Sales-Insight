#!/bin/bash

# Exit on any error
set -e

# Configuration
PROJECT_DIR="/Users/anujsiwach/Downloads/RabbitAI_FInal/Sales-Automator"

echo "=================================================="
echo "    Sales Insight Automator - Startup Script"
echo "=================================================="

# Go to project directory
cd "$PROJECT_DIR"

# 1. Check if Docker is running
echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker Desktop and try again."
  exit 1
fi

# 2. Check for .env file
echo "Checking environment variables..."
if [ ! -f .env ]; then
  echo "Warning: .env file not found. Creating from .env.example..."
  cp .env.example .env
  echo "Please edit the .env file with your API keys and SMTP credentials!"
  # We won't exit here so the user can still boot it, but the AI won't work
fi

# 3. Stop existing containers just in case
echo "Cleaning up any existing containers..."
docker-compose down

# 4. Build and start the stack
echo "Building and starting the containers..."
docker-compose up --build -d

echo ""
echo "=================================================="
echo "    Startup Complete! "
echo "=================================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend Docs: http://localhost:8000/docs"
echo ""
echo "To view logs, run: cd $PROJECT_DIR && docker-compose logs -f"
echo "To stop, run: cd $PROJECT_DIR && docker-compose down"
