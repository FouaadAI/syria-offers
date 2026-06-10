#!/bin/bash
set -e

echo "=== Syria Offers Production Server Setup ==="

# 1. System Update
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# 2. Install Docker & Docker Compose
echo "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker installed. Please log out and back in, then run this script again."
    exit 0
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    sudo apt install -y docker-compose-plugin
fi

# 3. Create app directory
mkdir -p ~/syria-offers
cd ~/syria-offers

# 4. Extract uploaded files (if using zip)
if [ -f ~/deploy.zip ]; then
    echo "Extracting deploy.zip..."
    unzip -o ~/deploy.zip -d ~/syria-offers/
    rm ~/deploy.zip
fi

# 5. Check if .env exists, if not copy example
if [ ! -f .env ]; then
    if [ -f .env.prod.example ]; then
        cp .env.prod.example .env
        echo "WARNING: Created .env from example. PLEASE EDIT IT WITH REAL VALUES!"
        echo "Run: nano ~/syria-offers/.env"
    fi
fi

# 6. Start services
echo "Starting Docker services..."
docker compose -f docker-compose.prod.yml up -d --build

echo ""
echo "=== Setup Complete ==="
echo "Backend API: http://91.144.32.230/api/v1"
echo "Web App: http://91.144.32.230/"
echo ""
echo "Check logs with: docker compose -f docker-compose.prod.yml logs -f"
echo "Edit .env with: nano ~/syria-offers/.env"