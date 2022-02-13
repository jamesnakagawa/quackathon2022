import discord
from discord.ext import commands
import os
from aiohttp import *
from dotenv import load_dotenv

# Load .env file with token
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents().all()
intents.members = True
intents.presences = True
intents.reactions = True

client = commands.Bot(command_prefix='$', intents=intents)
