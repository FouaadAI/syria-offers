#!/bin/bash
set -e

echo "=== Flutter Server Installation ==="

# 1. Install dependencies
sudo apt-get update -y
sudo apt-get install -y curl git unzip xz-utils zip libglu1-mesa

# 2. Install Flutter if not exists
if ! command -v flutter &> /dev/null; then
    echo "Installing Flutter SDK..."
    cd ~
    git clone https://github.com/flutter/flutter.git -b stable --depth 1
    echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
    export PATH="$PATH:$HOME/flutter/bin"
    flutter precache
    flutter doctor
    echo "Flutter installed. Please run: source ~/.bashrc"
else
    echo "Flutter already installed: $(flutter --version)"
fi

# 3. Enable web support
flutter config --enable-web

echo ""
echo "=== DONE ==="
echo "Flutter version: $(flutter --version | head -1)"
echo "Next: run ./scripts/build-and-deploy-web.sh"
