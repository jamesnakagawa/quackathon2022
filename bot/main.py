from aiohttp import *
from client import client, TOKEN

from commands import general, quacks, direct_messages, battle, duckmon, changesettings

# Run
client.run(TOKEN)
