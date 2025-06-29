import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
import random
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
        self.loop_mode = False

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
            self.loop_mode = False
            await ctx.send("Disconnected from voice channel!")
        else:
            await ctx.send("I'm not connected to a voice channel!")

    async def play_next(self, ctx):
        """Play the next song in the queue"""
        if self.queue:
            next_song = self.queue.pop(0)
            self.current_song = next_song['player']
            self.is_playing = True
            
            # Create embed for next song
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"**{next_song['player'].title}**",
                color=0x00ff00
            )
            
            if next_song['player'].thumbnail:
                embed.set_thumbnail(url=next_song['player'].thumbnail)
            
            if next_song['player'].duration:
                minutes, seconds = divmod(next_song['player'].duration, 60)
                embed.add_field(name="Duration", value=f"{int(minutes):02d}:{int(seconds):02d}", inline=True)
            
            embed.add_field(name="Requested by", value=next_song['requester'], inline=True)
            embed.add_field(name="Queue Position", value=f"Playing now", inline=True)
            
            # Play with callback to play next song when finished
            ctx.voice_client.play(next_song['player'], after=lambda e: asyncio.run_coroutine_threadsafe(self.song_finished(ctx, e), self.bot.loop))
            
            await ctx.send(embed=embed)
        else:
            self.is_playing = False
            self.current_song = None
            await ctx.send("🎵 Queue is empty! Add more songs with `!play <song>`")

    async def song_finished(self, ctx, error):
        """Called when a song finishes playing"""
        if error:
            print(f'Player error: {error}')
        
        if self.loop_mode and self.current_song:
            # If loop mode is on, add current song back to the beginning of queue
            self.queue.insert(0, {
                'player': self.current_song,
                'requester': "Loop mode"
            })
        
        # Play next song
        await self.play_next(ctx)

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
                
                # If nothing is currently playing, play immediately
                if not self.is_playing and not ctx.voice_client.is_playing():
                    self.current_song = player
                    self.is_playing = True
                    
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
                    
                    # Play the audio with callback for queue management
                    ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.song_finished(ctx, e), self.bot.loop))
                    
                    await ctx.send(embed=embed)
                else:
                    # Add to queue
                    queue_item = {
                        'player': player,
                        'requester': ctx.author.mention
                    }
                    self.queue.append(queue_item)
                    
                    # Create embed for queued song
                    embed = discord.Embed(
                        title="➕ Added to Queue",
                        description=f"**{player.title}**",
                        color=0x0099ff
                    )
                    
                    if player.thumbnail:
                        embed.set_thumbnail(url=player.thumbnail)
                    
                    if player.duration:
                        minutes, seconds = divmod(player.duration, 60)
                        embed.add_field(name="Duration", value=f"{int(minutes):02d}:{int(seconds):02d}", inline=True)
                    
                    embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                    embed.add_field(name="Queue Position", value=f"#{len(self.queue)}", inline=True)
                    
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
            self.queue.clear()  # Clear the queue when stopping
            await ctx.send("⏹️ Music stopped and queue cleared!")
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
            
            if len(self.queue) > 0:
                embed.add_field(name="Up Next", value=f"{len(self.queue)} song(s) in queue", inline=True)
            
            if self.loop_mode:
                embed.add_field(name="Loop Mode", value="✅ Enabled", inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("No music is currently playing!")

    @commands.command(name='queue', aliases=['q'], help='Show the current queue')
    async def show_queue(self, ctx):
        if not self.queue:
            if self.current_song and self.is_playing:
                embed = discord.Embed(
                    title="📋 Music Queue",
                    description="Queue is empty, but music is currently playing.\nUse `!np` to see current song.",
                    color=0x0099ff
                )
            else:
                embed = discord.Embed(
                    title="📋 Music Queue",
                    description="Queue is empty. Add songs with `!play <song>`",
                    color=0x0099ff
                )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📋 Music Queue",
            color=0x0099ff
        )
        
        queue_text = ""
        for i, item in enumerate(self.queue[:10], 1):  # Show first 10 songs
            duration_text = ""
            if item['player'].duration:
                minutes, seconds = divmod(item['player'].duration, 60)
                duration_text = f" ({int(minutes):02d}:{int(seconds):02d})"
            
            queue_text += f"**{i}.** {item['player'].title}{duration_text}\n   *Requested by {item['requester']}*\n\n"
        
        if len(self.queue) > 10:
            queue_text += f"... and {len(self.queue) - 10} more songs"
        
        embed.description = queue_text
        embed.add_field(name="Total Songs", value=str(len(self.queue)), inline=True)
        
        if self.current_song and self.is_playing:
            embed.add_field(name="Now Playing", value=self.current_song.title, inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='skip', aliases=['next'], help='Skip the current song')
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # This will trigger the after callback and play next song
            await ctx.send("⏭️ Skipped current song!")
        else:
            await ctx.send("No music is currently playing!")

    @commands.command(name='clear', help='Clear the queue')
    async def clear_queue(self, ctx):
        if self.queue:
            cleared_count = len(self.queue)
            self.queue.clear()
            await ctx.send(f"🗑️ Cleared {cleared_count} song(s) from the queue!")
        else:
            await ctx.send("Queue is already empty!")

    @commands.command(name='remove', help='Remove a song from queue by position')
    async def remove_from_queue(self, ctx, position: int):
        if not self.queue:
            await ctx.send("Queue is empty!")
            return
        
        if position < 1 or position > len(self.queue):
            await ctx.send(f"Invalid position! Queue has {len(self.queue)} songs.")
            return
        
        removed_song = self.queue.pop(position - 1)
        await ctx.send(f"🗑️ Removed **{removed_song['player'].title}** from position {position}")

    @commands.command(name='shuffle', help='Shuffle the queue')
    async def shuffle_queue(self, ctx):
        if len(self.queue) < 2:
            await ctx.send("Need at least 2 songs in queue to shuffle!")
            return
        
        random.shuffle(self.queue)
        await ctx.send(f"🔀 Shuffled {len(self.queue)} songs in the queue!")

    @commands.command(name='loop', help='Toggle loop mode for current song')
    async def toggle_loop(self, ctx):
        self.loop_mode = not self.loop_mode
        status = "enabled" if self.loop_mode else "disabled"
        emoji = "🔁" if self.loop_mode else "❌"
        await ctx.send(f"{emoji} Loop mode {status}!")

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
