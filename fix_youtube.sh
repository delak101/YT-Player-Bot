#!/bin/bash

# YouTube Bot Detection Fix Script
# Run this script to fix "Sign in to confirm you're not a bot" errors

echo "🤖 Fixing YouTube bot detection issues..."

# Stop the bot service
sudo systemctl stop discord-bot

cd /opt/discord-bot
source venv/bin/activate

# Update yt-dlp to the absolute latest version
echo "📦 Updating yt-dlp..."
pip install --upgrade --force-reinstall yt-dlp

# Install additional dependencies for better YouTube compatibility
pip install --upgrade requests[socks] fake-useragent

# Create enhanced configuration for yt-dlp
echo "⚙️  Creating enhanced YouTube configuration..."

# Update .env with additional settings
cat >> .env << 'EOF'

# YouTube Bot Detection Bypass
YT_DLP_NO_CHECK_CERTIFICATE=1
YT_DLP_IGNORE_ERRORS=1
YT_DLP_PREFER_INSECURE=1
YT_DLP_FORCE_JSON=1
EOF

# Create a custom yt-dlp config file
mkdir -p ~/.config/yt-dlp
cat > ~/.config/yt-dlp/config << 'EOF'
# YouTube bot detection bypass configuration
--no-check-certificate
--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
--referer "https://www.youtube.com/"
--add-header "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
--add-header "Accept-Language:en-us,en;q=0.5"
--add-header "Sec-Fetch-Mode:navigate"
--prefer-insecure
--no-warnings
--ignore-errors
--extractor-args "youtube:player_client=android,web"
--extractor-args "youtube:skip=dash,hls"
EOF

# Update the systemd service with enhanced settings
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
Environment=YT_DLP_NO_CHECK_CERTIFICATE=1
Environment=REQUESTS_CA_BUNDLE=""
Environment=HOME=/root
ExecStart=/opt/discord-bot/venv/bin/python bot.py
Restart=always
RestartSec=15
RestartPreventExitStatus=1

[Install]
WantedBy=multi-user.target
EOF

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl start discord-bot

echo "✅ YouTube bot detection fixes applied!"
echo "📊 Checking service status..."
sleep 5

if sudo systemctl is-active --quiet discord-bot; then
    echo "🎉 Bot is running!"
    echo "📋 Monitor: sudo journalctl -u discord-bot -f"
    echo ""
    echo "🧪 Test with search queries instead of URLs:"
    echo "!play never gonna give you up"
    echo "!play rick astley"
    echo "!play despacito"
else
    echo "❌ Service issues. Check logs:"
    sudo journalctl -u discord-bot --no-pager -n 15
fi
