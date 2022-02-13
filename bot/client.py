import discord
from discord.ext import commands
import os
from bot.models import DuckType
import models
import random
from aiohttp import *
from dotenv import load_dotenv
from models import Session

# Load .env file with token
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents().all()
intents.members = True
intents.presences = True
intents.reactions = True

session = Session()
client = commands.Bot(command_prefix='$', intents=intents)

# Load ducks into database
session.add_all([
DuckType(name = "Giles", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Kelsie", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Reese", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Bertha", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Lily", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Shakir", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Geese", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Clifford", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12)),
DuckType(name = "Lilia", attack_coeff = random.randint(15, 30), defend_coeff = random.randint(5, 12))])

#query_array = [duck_type1, duck_type2, duck_type3, duck_type4, duck_type5, duck_type6, duck_type7, duck_type8, duck_type9]

session.query(DuckType).count(9)
session.commit()

