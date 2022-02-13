from client import client
from lib import duckmon
import discord
from aiohttp import *

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
    spawnFunc(ctx)

async def spawnFunc(ctx):
    API = "https://random-d.uk/api/v2/random"
    async with request("GET", API, headers={}) as response:
        if response.status == 200:
            buffer = await response.json()
            duckValue = buffer['url']
            stats = duckmon.get_specific_duck()
            c = stats[4]
            embed = discord.Embed(title="A Duck has spawned", description="ID: {} \nMood: {} \nAttack: {}\nDefence: {}".format(
                stats[0], stats[1], stats[2], stats[3]), color=discord.Color.from_rgb(c[0], c[1], c[2]))
            embed.set_image(url=duckValue)
            reaction = await ctx.send(embed=embed)
            await reaction.add_reaction(emoji = '\N{THUMBS UP SIGN}')
        else:
            await ctx.send("Error getting image. API returned {}".format(response.status))
