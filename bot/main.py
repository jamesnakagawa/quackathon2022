import imp
from unicodedata import name
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
import os
import json
from aiohttp import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$duck'):
        await message.channel.send('Quack!')

client.run(TOKEN)


@client.command(name='ducky', help='Loads a duck image')
async def ducky(ctx):
    API = "https://random-d.uk/api/v2/random"
    async with request("GET", API, headers={}) as response:
        if response.status == 200:
            buffer = await response.json()
            url = buffer['url']
            await ctx.send(url)
        else:
            await ctx.send("Error getting image. API returned {}".format(response.status))

client.run(os.getenv('TOKEN'))
