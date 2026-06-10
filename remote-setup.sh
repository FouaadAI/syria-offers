#!/bin/bash
set -e

echo "=== Syria Offers Server Setup ==="

# 1. Update system
sudo apt update -y

# 2. Install Docker if not exists
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker installed. Please log out and back in, then run this script again."
    exit 0
fi

# 3. Install docker compose plugin if not exists
if ! docker compose version &> /dev/null; then
    sudo apt install -y docker-compose-plugin
fi

# 4. Clone or update repo
if [ -d ~/syria-offers ]; then
    echo "Updating existing repo..."
    cd ~/syria-offers
    git pull
else
    echo "Cloning repo..."
    git clone https://github.com/FouaadAI/syria-offers.git ~/syria-offers
    cd ~/syria-offers
fi

# 5. Go to backend
cd backend

# 6. Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.prod.example .env
    # Generate random secret key
    SECRET=$(openssl rand -hex 32)
    sed -i "s/change-me-to-a-very-long-random-string-at-least-32-characters/$SECRET/g" .env
    sed -i "s/CHANGE_THIS_TO_STRONG_PASSWORD/$(openssl rand -hex 16)/g" .env
    sed -i "s/your-gemini-api-key-here/AIzaSyDIJ4rCAVMuePyng1EtX89Vc3KqBPHluHY/g" .env
    sed -i "s/your-mail-password-here/xsmtpsib-b4d3ca87558a5fdd2f39e94bf65670ace9b38185e2f5c593183fa50f614af7e2-WiYMHqmkcVJ2mVSz/g" .env
    echo ""
    echo "=== .env CREATED ==="
    echo "Please check it with: nano ~/syria-offers/backend/.env"
fi

# 7. Build and start
echo "Starting services..."
docker compose -f docker-compose.prod.yml up -d --build

# 8. Wait a moment
sleep 10

# 9. Check status
echo ""
echo "=== STATUS ==="
docker compose -f docker-compose.prod.yml ps

echo ""
echo "=== ACCESS ==="
echo "Web App: http://91.144.32.230/"
echo "API: http://91.144.32.230/api/v1"
echo "Health: http://91.144.32.230/health"
echo ""
echo "Logs: docker compose -f docker-compose.prod.yml logs -f"
echo ""