@echo off
echo.
echo ================================
echo Discord Music Bot Setup Helper
echo ================================
echo.
echo STEP 1: Get your bot ready
echo 1. Go to https://discord.com/developers/applications
echo 2. Create New Application (give it a name)
echo 3. Go to Bot section and click "Add Bot"
echo 4. IMPORTANT: Enable "Message Content Intent"
echo 5. Copy your bot token
echo.
echo STEP 2: Set your bot token
echo Run this command with your actual token:
echo $env:DISCORD_BOT_TOKEN="your_token_here"
echo.
echo STEP 3: Generate invite link
echo Run: python generate_invite.py
echo.
echo STEP 4: Test your bot
echo After setting token, run: run_bot.bat
echo.
echo Press any key to continue...
pause > nul
