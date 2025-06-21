
import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import yt_dlp
import asyncio

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    await asyncio.sleep(5)
    channel = bot.get_channel(CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = await channel.connect()
            print(f"🎧 Joined voice channel: {channel.name}")
        except discord.ClientException as e:
            print(f"❌ Already connected: {e}")
        except discord.OpusNotLoaded as e:
            print(f"❌ Opus library not loaded: {e}")
        except discord.errors.ClientException as e:
            print(f"❌ Voice connect error: {e}")
        except Exception as e:
            print(f"❌ Unknown error when joining voice: {e}")
    else:
        print("❌ Channel not found or is not a voice channel.")

@bot.command()
async def play(ctx, url: str):
    if ctx.author.voice:
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        vc = ctx.voice_client

        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': 'song.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            source = discord.FFmpegPCMAudio("song.mp3")
            vc.play(source)
            await ctx.send(f"🎶 Now playing: {info['title']}")
    else:
        await ctx.send("❌ You need to be in a voice channel to play music.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Music stopped.")

keep_alive()
bot.run(TOKEN)
