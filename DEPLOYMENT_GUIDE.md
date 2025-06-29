# Discord Music Bot Deployment Guide

## Overview
This Discord music bot requires a persistent server environment and cannot be deployed on Vercel due to its serverless nature. Below are recommended hosting options.

## Recommended Hosting Platforms

### 1. DigitalOcean Droplet ($5-10/month)
- Ubuntu 22.04 LTS
- 1GB RAM minimum
- Persistent storage
- Full root access

### 2. AWS EC2 (Free tier available)
- t2.micro instance
- 1 year free tier
- Scalable resources

### 3. Google Cloud Compute Engine
- e2-micro instance
- $300 free credits
- Global infrastructure

### 4. Railway.app
- Easy deployment
- Built-in monitoring
- Automatic scaling

### 5. Render.com
- Simple setup
- Free tier available
- Automatic deployments

## Quick Deployment (DigitalOcean)

### Prerequisites
- DigitalOcean account
- SSH key configured
- Bot token from Discord Developer Portal

### Steps
1. Create Ubuntu 22.04 droplet
2. Upload bot files to server
3. Run deployment script: `chmod +x deploy.sh && ./deploy.sh`
4. Enter bot token when prompted
5. Bot will start automatically and restart on server reboot

### File Structure on Server
```
/opt/discord-bot/
├── bot.py
├── requirements.txt
├── deployment_requirements.txt
├── deploy.sh
├── venv/
└── .env
```

### Service Management
```bash
# Check status
sudo systemctl status discord-bot

# Start/stop/restart
sudo systemctl start discord-bot
sudo systemctl stop discord-bot
sudo systemctl restart discord-bot

# View logs
sudo journalctl -u discord-bot -f
```

### Environment Variables
Set the following environment variable:
- `DISCORD_BOT_TOKEN`: Your Discord bot token

### Required System Packages
- python3
- python3-pip
- python3-venv
- ffmpeg
- git

### Security Considerations
- Use SSH keys instead of passwords
- Configure firewall (ufw)
- Regular system updates
- Bot token security

### Monitoring
- System logs: `sudo journalctl -u discord-bot`
- Resource usage: `htop`
- Network status: `netstat -tlnp`

### Troubleshooting
- Check bot token validity
- Verify FFmpeg installation
- Check Discord API status
- Review system resources

## Alternative: Container Deployment

### Docker
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bot.py .
CMD ["python", "bot.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  discord-bot:
    build: .
    environment:
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
    restart: unless-stopped
```
