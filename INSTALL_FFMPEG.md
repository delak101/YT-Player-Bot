# FFmpeg Installation Guide for Discord Bot

## The Issue
Your Discord bot is running but can't play audio because FFmpeg is missing.
Error: "ffmpeg was not found"

## Solution: Install FFmpeg

### Option 1: Using Chocolatey (Recommended - Easiest)
1. Open PowerShell as Administrator
2. Install Chocolatey (if not already installed):
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Install FFmpeg:
   ```powershell
   choco install ffmpeg
   ```
4. Restart your terminal/PowerShell

### Option 2: Using winget (Windows Package Manager)
1. Open PowerShell as Administrator
2. Run:
   ```powershell
   winget install ffmpeg
   ```

### Option 3: Manual Installation
1. Go to: https://www.gyan.dev/ffmpeg/builds/
2. Download: "release builds" -> "ffmpeg-release-essentials.zip"
3. Extract to: C:\ffmpeg
4. Add to PATH:
   - Right-click "This PC" -> Properties
   - Advanced system settings -> Environment Variables
   - Under "System variables", find "Path" -> Edit
   - Add: C:\ffmpeg\bin
   - Click OK and restart terminal

### Option 4: Quick Download (Alternative)
1. Download from: https://github.com/BtbN/FFmpeg-Builds/releases
2. Get: "ffmpeg-master-latest-win64-gpl.zip"
3. Extract and add bin folder to PATH

## After Installation
1. Restart your PowerShell terminal
2. Test: `ffmpeg -version`
3. Restart your Discord bot
4. Try the !play command again

## Quick Test Commands
After installing FFmpeg:
```powershell
# Test FFmpeg
ffmpeg -version

# Restart bot
python bot.py

# Test in Discord
!play https://youtu.be/apZwCXy8E9U?si=4DpUMI0XoXkhaS0S
```

## Troubleshooting
- If FFmpeg still not found: Restart your computer
- Make sure you added the bin folder (not just ffmpeg folder) to PATH
- Use full path: C:\ffmpeg\bin (not C:\ffmpeg)
