import discord
from discord.ext import commands
from discord_slash import SlashCommand
import os
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
