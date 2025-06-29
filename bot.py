import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
from typing import Optional

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# YouTube DL options
ytdl_format_options = {
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

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client: Optional[discord.VoiceClient] = None
        self.queue = []
        self.current_song = None
        self.is_playing = False

    @commands.command(name='join', help='Bot joins your voice channel')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return
        
        channel = ctx.author.voice.channel
        
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            self.voice_client = await channel.connect()
        
        await ctx.send(f"Joined {channel.name}!")

    @commands.command(name='leave', help='Bot leaves the voice channel')
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.voice_client = None
            self.queue.clear()
            self.current_song = None
            self.is_playing = False
            await ctx.send("Disconnected from voice channel!")
        else:
            await ctx.send("I'm not connected to a voice channel!")

    @commands.command(name='play', help='Play a song from YouTube')
    async def play(self, ctx, *, url):
        if not ctx.voice_client:
            if ctx.author.voice:
                await self.join(ctx)
            else:
                await ctx.send("You need to be in a voice channel to play music!")
                return

        try:
            # Show that bot is processing
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                
                # Create embed for song info
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"**{player.title}**",
                    color=0x00ff00
                )
                
                if player.thumbnail:
                    embed.set_thumbnail(url=player.thumbnail)
                
                if player.duration:
                    minutes, seconds = divmod(player.duration, 60)
                    embed.add_field(name="Duration", value=f"{int(minutes):02d}:{int(seconds):02d}", inline=True)
                
                embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                
                # Play the audio
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                self.current_song = player
                self.is_playing = True
                
                await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='pause', help='Pause the current song')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Music paused!")
        else:
            await ctx.send("No music is currently playing!")

    @commands.command(name='resume', help='Resume the paused song')
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Music resumed!")
        else:
            await ctx.send("Music is not paused!")

    @commands.command(name='stop', help='Stop the current song')
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            self.current_song = None
            self.is_playing = False
            await ctx.send("⏹️ Music stopped!")
        else:
            await ctx.send("No music is currently playing!")

    @commands.command(name='volume', help='Change the volume (0-100)')
    async def volume(self, ctx, volume: int):
        if not ctx.voice_client:
            await ctx.send("I'm not connected to a voice channel!")
            return
        
        if not 0 <= volume <= 100:
            await ctx.send("Volume must be between 0 and 100!")
            return
        
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"🔊 Volume set to {volume}%")
        else:
            await ctx.send("No audio is currently playing!")

    @commands.command(name='nowplaying', aliases=['np'], help='Show current playing song')
    async def now_playing(self, ctx):
        if self.current_song and self.is_playing:
            embed = discord.Embed(
                title="🎵 Currently Playing",
                description=f"**{self.current_song.title}**",
                color=0x00ff00
            )
            
            if self.current_song.thumbnail:
                embed.set_thumbnail(url=self.current_song.thumbnail)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("No music is currently playing!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to play music!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found! Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument! Please check the command usage.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

@bot.event
async def setup_hook():
    """This is called when the bot is starting up"""
    await bot.add_cog(MusicBot(bot))
    print("Music cog loaded successfully!")

if __name__ == "__main__":
    # Load bot token from environment variable
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN environment variable not found!")
        print("Please set your Discord bot token as an environment variable.")
        print("Example: $env:DISCORD_BOT_TOKEN=\"your_token_here\"")
        exit(1)
    else:
        bot.run(TOKEN)
