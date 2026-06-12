#!/bin/bash
set -e

echo "=== Syria Offers Flutter Web Build & Deploy ==="

# Ensure Flutter is in PATH
export PATH="$PATH:$HOME/flutter/bin"

# Verify Flutter
flutter --version

# 1. Go to project
cd ~/syria-offers

# 2. Pull latest changes (ensure correct version)
echo "Pulling latest changes from GitHub..."
git pull origin master

# 3. Go to Flutter app
cd syria_offers_app

# 4. Get dependencies
echo "Getting Flutter dependencies..."
flutter pub get

# 5. Build web
echo "Building Flutter Web..."
flutter build web --release

# 6. Deploy to nginx web directory
echo "Deploying to backend/web..."
rm -rf ~/syria-offers/backend/web
mkdir -p ~/syria-offers/backend/web
cp -r build/web/* ~/syria-offers/backend/web/

# 7. Restart nginx container
echo "Restarting nginx..."
cd ~/syria-offers/backend
docker compose -f docker-compose.prod.yml restart nginx

# 8. Verify
echo ""
echo "=== DEPLOY COMPLETE ==="
echo "Web files: ~/syria-offers/backend/web/"
docker compose -f docker-compose.prod.yml ps nginx
echo ""
echo "Access: http://91.144.32.230/"
