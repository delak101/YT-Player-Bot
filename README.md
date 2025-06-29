# Discord YouTube Music Bot

A Discord bot that can play audio from YouTube videos in voice channels.

## Features

- 🎵 Play audio from YouTube videos
- ⏸️ Pause/Resume functionality
- ⏹️ Stop playback
- 🔊 Volume control
- 📋 Show currently playing song
- 🎯 Auto-join voice channels

## Commands

- `!join` - Bot joins your current voice channel
- `!leave` - Bot leaves the voice channel
- `!play <YouTube URL or search term>` - Play audio from YouTube
- `!pause` - Pause the current song
- `!resume` - Resume the paused song
- `!stop` - Stop the current song
- `!volume <0-100>` - Set the volume (0-100%)
- `!nowplaying` or `!np` - Show the currently playing song

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the bot token (you'll need this later)
6. Under "Privileged Gateway Intents", enable "Message Content Intent"

### 2. Install FFmpeg

FFmpeg is required for audio processing:

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract the files and add the `bin` folder to your system PATH
3. Or download from https://github.com/BtbN/FFmpeg-Builds/releases

**Alternative for Windows:**
```powershell
# Using chocolatey
choco install ffmpeg

# Using winget
winget install ffmpeg
```

### 3. Set up the Bot Token

Set your Discord bot token as an environment variable:

**Windows (PowerShell):**
```powershell
$env:DISCORD_BOT_TOKEN="your_bot_token_here"
```

**Windows (Command Prompt):**
```cmd
set DISCORD_BOT_TOKEN=your_bot_token_here
```

**For permanent setup, add it to your system environment variables through Control Panel.**

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Run the Bot

```powershell
python bot.py
```

## Bot Permissions

When inviting the bot to your server, make sure it has these permissions:
- Read Messages
- Send Messages
- Connect (to voice channels)
- Speak (in voice channels)
- Use Voice Activity

## Usage Examples

```
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
!play Never Gonna Give You Up Rick Astley
!pause
!resume
!volume 50
!stop
!leave
```

## Troubleshooting

### Common Issues:

1. **"FFmpeg not found"**
   - Make sure FFmpeg is installed and added to your system PATH

2. **"Bot not responding"**
   - Check if the bot token is correctly set
   - Ensure the bot has proper permissions in your Discord server

3. **"Cannot connect to voice channel"**
   - Make sure you're in a voice channel when using `!play`
   - Check if the bot has permission to connect to voice channels

4. **"Audio not playing"**
   - Ensure you have a stable internet connection
   - Some YouTube videos may be restricted or unavailable

### Debug Mode:
To see more detailed error messages, you can modify the bot.py file to enable debug logging.

## Notes

- The bot uses yt-dlp to extract audio from YouTube videos
- Audio is streamed in real-time (not downloaded)
- The bot supports both direct YouTube URLs and search terms
- Only one song can play at a time (no queue system in this basic version)

## License

This project is open source and available under the MIT License.
