
import discord
from discord.ext import commands, tasks
import asyncio
import os
import yt_dlp
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f"✅ {bot.user.name} is online.")
    ensure_connected.start()

@tasks.loop(minutes=1)
async def ensure_connected():
    try:
        for guild in bot.guilds:
            channel = guild.get_channel(CHANNEL_ID)
            if channel and (not guild.voice_client or not guild.voice_client.is_connected()):
                await channel.connect()
    except Exception as e:
        print("Bot Error in ensure_connected:", e)

@bot.command()
async def play(ctx, *, url):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice:
        if ctx.author.voice:
            voice = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You're not in a voice channel.")
            return

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': 'True',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        voice.stop()
        voice.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
        await ctx.send(f"🎶 Now playing: {info['title']}")
    except Exception as e:
        print("Playback Error:", e)
        await ctx.send("❌ Could not play the audio.")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("⏹️ Stopped the music.")

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice:
        await voice.disconnect()
        await ctx.send("👋 Left the voice channel.")

keep_alive()
bot.run(TOKEN)
