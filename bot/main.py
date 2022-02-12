import imp
from unicodedata import name
import discord
from discord.ext import commands, tasks
import os
import json
from aiohttp import *
from dotenv import load_dotenv
import duckmon

# Load .env file with token
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents().all()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='$', intents=intents)

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
    elif message.content == "status":
        await message.channel.send('Quackmon!')

    await client.process_commands(message)

# bot commands


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


@client.command(name="spawn", help="Spawns a random duck")
async def spawn(ctx):
    API = "https://random-d.uk/api/v2/random"
    async with request("GET", API, headers={}) as response:
        if response.status == 200:
            buffer = await response.json()
            duckValue = buffer['url']
            stats = duckmon.get_specific_duck()
            embed = discord.Embed(title="A Duck has spawned", description="ID: {} \nMood: {} \nAttack: {}\nDefence: {}".format(
                stats[0], stats[1], stats[2], stats[3]))
            # color=discord.Color.from_rgb(stats[4])
            embed.set_image(url=duckValue)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Error getting image. API returned {}".format(response.status))


@client.command()
async def shutdown(ctx):
    client.logout()
    client.close()
    exit()


# Run
client.run(os.getenv('TOKEN'))
