from aiohttp import *
from client import client, TOKEN

from commands import general, quacks, direct_messages, battle, duckmon

# Run
client.run(TOKEN)
