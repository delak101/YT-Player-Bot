# Bot Update Instructions for YouTube Bot Detection Fix

## Replace the YouTube DL configuration in bot.py

Find this section in your bot.py:
```python
# YouTube DL options
ytdl_format_options = {
    ...
}
```

Replace it with this enhanced configuration:

```python
# Enhanced YouTube DL options for bot detection bypass
ytdl_format_options = {
    'format': 'worstaudio/worst',  # Use worst quality for better compatibility
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',  # Always search instead of direct URLs
    'source_address': '0.0.0.0',
    'force_ssl': False,
    'prefer_insecure': True,
    'socket_timeout': 10,
    'retries': 2,
    'fragment_retries': 2,
    'extractor_args': {
        'youtube': {
            'skip': ['dash', 'hls'],
            'player_client': ['android_music', 'android'],
            'player_skip': ['configs', 'webpage']
        }
    },
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }
}
```

## Update the play command logic

Also find the play command and modify it to always use search:

```python
@commands.command(name='play', help='Play a song from YouTube')
async def play(self, ctx, *, url):
    if not ctx.voice_client:
        if ctx.author.voice:
            await self.join(ctx)
        else:
            await ctx.send("You need to be in a voice channel to play music!")
            return

    try:
        async with ctx.typing():
            # Always convert to search query for better compatibility
            search_query = url
            
            # If it's a URL, extract title/ID for search
            if 'youtube.com' in url or 'youtu.be' in url:
                # Extract video ID and search by ID
                if 'watch?v=' in url:
                    video_id = url.split('watch?v=')[1].split('&')[0]
                    search_query = f"ytsearch:{video_id}"
                elif 'youtu.be/' in url:
                    video_id = url.split('youtu.be/')[1].split('?')[0]
                    search_query = f"ytsearch:{video_id}"
            else:
                # Regular search query
                search_query = f"ytsearch:{url}"
            
            # Rest of your existing play logic...
            player = await YTDLSource.from_url(search_query, loop=self.bot.loop, stream=True)
            
            # Continue with existing queue logic...
```

## Instructions for server:

1. Upload the updated bot.py to your server
2. Run the fix_youtube.sh script:
   ```bash
   cd /opt/discord-bot
   chmod +x fix_youtube.sh
   sudo ./fix_youtube.sh
   ```

3. The bot will restart with enhanced YouTube compatibility

## Key Changes:
- Uses worst quality audio for maximum compatibility
- Always converts URLs to search queries
- Uses Android mobile client user agent
- Reduced timeouts and retries for faster fallback
- Enhanced headers to avoid bot detection
