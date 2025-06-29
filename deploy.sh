#!/bin/bash

# Discord Bot Deployment Script
# Run this on your server after uploading the bot files

echo "Setting up Discord Music Bot..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv ffmpeg git -y

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r deployment_requirements.txt

# Get bot token securely
echo "Please enter your Discord bot token:"
echo "Go to: https://discord.com/developers/applications"
echo "Select your bot -> Bot section -> Reset Token"
read -s BOT_TOKEN

# Validate token format
if [[ ! $BOT_TOKEN =~ ^[A-Za-z0-9._-]{24}\.[A-Za-z0-9._-]{6}\.[A-Za-z0-9._-]{27}$ ]]; then
    echo "⚠️  Warning: Token format doesn't look correct"
    echo "Expected format: MTxxxxx.xxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo "Continue anyway? (y/n)"
    read -n 1 continue
    if [[ $continue != "y" ]]; then
        echo "Deployment cancelled"
        exit 1
    fi
fi

# Create .env file with comprehensive settings
echo "DISCORD_BOT_TOKEN=$BOT_TOKEN" > .env
echo "PYTHONHTTPSVERIFY=0" >> .env
echo "SSL_VERIFY=false" >> .env
echo "YT_DLP_NO_CHECK_CERTIFICATE=1" >> .env
chmod 600 .env

# Apply YouTube bypass fixes
echo "🎵 Applying YouTube detection bypasses..."

# Update yt-dlp to latest version
pip install --upgrade yt-dlp

# Install additional packages for better compatibility
pip install --upgrade requests urllib3 certifi

# Create systemd service with enhanced environment
sudo tee /etc/systemd/system/discord-bot.service > /dev/null <<EOF
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
EnvironmentFile=$(pwd)/.env
Environment=PYTHONHTTPSVERIFY=0
Environment=SSL_VERIFY=false
Environment=YT_DLP_NO_CHECK_CERTIFICATE=1
Environment=REQUESTS_CA_BUNDLE=""
ExecStart=$(pwd)/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot

# Wait a moment and check status
sleep 3
if sudo systemctl is-active --quiet discord-bot; then
    echo "✅ Bot deployed successfully!"
    echo "📊 Status: sudo systemctl status discord-bot"
    echo "📋 Logs: sudo journalctl -u discord-bot -f"
    echo "🔗 Invite link: https://discord.com/api/oauth2/authorize?client_id=1388868051222532149&permissions=37080064&scope=bot"
else
    echo "❌ Deployment failed. Check logs:"
    sudo journalctl -u discord-bot --no-pager -n 20
fi
