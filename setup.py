#!/usr/bin/env python3
"""
Setup script for Discord Music Bot
This script helps you set up the bot token and verify the installation.
"""

import os
import sys

def main():
    print("🎵 Discord Music Bot Setup 🎵")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check if virtual environment is active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Virtual environment not detected. Consider using one for better package management.")
    
    # Check for required packages
    try:
        import discord
        print("✅ discord.py is installed")
    except ImportError:
        print("❌ discord.py not found. Run: pip install -r requirements.txt")
        return False
    
    try:
        import yt_dlp
        print("✅ yt-dlp is installed")
    except ImportError:
        print("❌ yt-dlp not found. Run: pip install -r requirements.txt")
        return False
    
    # Check for bot token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        print("✅ Discord bot token found in environment variables")
    else:
        print("⚠️  Discord bot token not found!")
        print("Please set your bot token as an environment variable:")
        print("Windows PowerShell: $env:DISCORD_BOT_TOKEN=\"your_token_here\"")
        print("Windows CMD: set DISCORD_BOT_TOKEN=your_token_here")
        
        # Offer to set it temporarily
        user_token = input("\nEnter your Discord bot token (or press Enter to skip): ").strip()
        if user_token:
            os.environ['DISCORD_BOT_TOKEN'] = user_token
            print("✅ Token set for this session")
        else:
            print("⚠️  You'll need to set the token before running the bot")
    
    print("\n🚀 Setup complete!")
    print("Run the bot with: python bot.py")
    print("Or use the batch file: run_bot.bat")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
