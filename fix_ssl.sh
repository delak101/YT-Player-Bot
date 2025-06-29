#!/bin/bash

# SSL Certificate Fix Script for Discord Bot
# Run this script on your DigitalOcean server to fix SSL issues

echo "🔧 Fixing SSL Certificate Issues..."

# Stop the bot service
sudo systemctl stop discord-bot

# Update system and certificates
echo "📦 Updating system and certificates..."
sudo apt update
sudo apt install -y ca-certificates curl wget

# Update CA certificates
sudo update-ca-certificates

# Install latest OpenSSL
sudo apt install -y openssl libssl-dev

# Fix Python SSL certificates
echo "🐍 Fixing Python SSL certificates..."
cd /opt/discord-bot

# Activate virtual environment
source venv/bin/activate

# Update pip and certificates
pip install --upgrade pip
pip install --upgrade certifi requests urllib3

# Install pyOpenSSL for better SSL handling
pip install pyOpenSSL>=23.0.0

# Update yt-dlp to latest version
pip install --upgrade yt-dlp

# Set environment variables for SSL bypass
echo "🌍 Setting SSL environment variables..."
echo "export PYTHONHTTPSVERIFY=0" >> ~/.bashrc
echo "export SSL_VERIFY=false" >> ~/.bashrc
echo "export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt" >> ~/.bashrc

# Update .env file with SSL settings
if [ -f .env ]; then
    echo "" >> .env
    echo "# SSL Configuration" >> .env
    echo "PYTHONHTTPSVERIFY=0" >> .env
    echo "SSL_VERIFY=false" >> .env
    echo "REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt" >> .env
fi

# Update systemd service with SSL environment variables
echo "⚙️  Updating systemd service..."
sudo tee /etc/systemd/system/discord-bot.service > /dev/null <<EOF
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/discord-bot
EnvironmentFile=/opt/discord-bot/.env
Environment=PYTHONHTTPSVERIFY=0
Environment=SSL_VERIFY=false
Environment=REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ExecStart=/opt/discord-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start discord-bot

echo "✅ SSL fixes applied!"
echo "📊 Checking service status..."
sleep 3

if sudo systemctl is-active --quiet discord-bot; then
    echo "🎉 Bot is running successfully!"
    echo "📋 Monitor logs: sudo journalctl -u discord-bot -f"
else
    echo "❌ Service not running. Check logs:"
    sudo journalctl -u discord-bot --no-pager -n 10
fi

echo ""
echo "🧪 Test the bot with these commands in Discord:"
echo "!join"
echo "!play never gonna give you up"
echo "!queue"
