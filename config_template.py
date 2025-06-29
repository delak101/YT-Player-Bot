# Configuration file for Discord Music Bot
# Copy this file to config.py and fill in your values

# Discord Bot Configuration
BOT_TOKEN = "your_discord_bot_token_here"
COMMAND_PREFIX = "!"

# Audio Configuration
DEFAULT_VOLUME = 0.5  # 50% volume
MAX_VOLUME = 1.0      # 100% volume

# YouTube DL Configuration
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

# FFmpeg Configuration
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
