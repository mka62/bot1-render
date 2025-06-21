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
        
