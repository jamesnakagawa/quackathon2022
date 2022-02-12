import imp
from unicodedata import name
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
import os
import json
from aiohttp import *
from dotenv import load_dotenv

# Load .env file with token
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents().all()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='$', intents=intents)
slash = SlashCommand(client, sync_commands=True)

# On start
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# On message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "duck":
        await message.channel.send('Quack!')

    await client.process_commands(message)

<<<<<<< HEAD
# bot commands
=======

@slash.slash(name="Verify", description="Posts a random duck image!")
>>>>>>> 4d34bf520fa658f92d61e653b407b86daa381645
@client.command(name="ducky", help="Posts a random duck image")
async def ducky(ctx):
    API = "https://random-d.uk/api/v2/random"
    async with request("GET", API, headers={}) as response:
        if response.status == 200:
            buffer = await response.json()
            url = buffer['url']
            await ctx.send(f"{ctx.author.mention} Here's your ducky!")
            await ctx.send(url)
        else:
            await ctx.send("Error getting image. API returned {}".format(response.status))

# Run
client.run(os.getenv('TOKEN'))
