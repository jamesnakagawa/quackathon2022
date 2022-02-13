import discord
from aiohttp import *

from client import client, slash, session
from models import Player
import duckmon

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
        await message.channel.send('Quack!!')

    await client.process_commands(message)

# bot commands


@slash.slash(name="Verify", description="Posts a random duck image!")
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
            user = session.query(Player).filter(Player.handle == ctx.author.name).one_or_none()
            stats = duckmon.get_specific_duck(user.id)
            embed = discord.Embed(title="A Duck has spawned", description="ID: {} \nMood: {} \nAttack: {}\nDefence: {}".format(
                stats[0], stats[1], stats[2], stats[3]), color=discord.Color.from_rgb(stats[4]))
            embed.set_image(url=duckValue)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Error getting image. API returned {}".format(response.status))


@client.command()
async def shutdown(ctx):
    exit()
