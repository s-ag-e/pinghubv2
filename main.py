import discord
from discord.ext import commands
import asyncio
import json
import threading

pingr = commands.Bot(command_prefix="_", help_command=None)

# full credits of this code goes to Geb#1337

with open("config.json") as f:
    geb = json.load(f)
with open("config.json") as f:
    guildid = int(geb["spam_guild_id"])
    roleid = geb["ping_role_id"]
    bottoken = geb["bot_token"]

async def ping_task():
    guild = pingr.get_guild(guildid)
    channels = [channel for channel in guild.channels if isinstance(channel, discord.TextChannel) and channel.name.startswith('ping')]
    while True:
        await asyncio.gather(*[channel.send(f"<@&{roleid}>") for channel in channels])
        await asyncio.sleep(0.1)

def run_ping_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ping_task())

@pingr.event
async def on_ready():
    threading.Thread(target=run_ping_task, daemon=True).start()

@pingr.slash_command(guild_ids=[guildid])
async def ping(ctx):
    await ctx.respond(f"{round(pingr.latency * 1000)}ms")

pingr.run(bottoken)
