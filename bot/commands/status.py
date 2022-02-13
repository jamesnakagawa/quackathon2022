from client import *
import json


@client.command(name="status", description="prints out bot status and content of settings.json")
async def status(ctx):
    json_file = open('bot/settings.json', 'r', encoding="utf-8")
    data = json.load(json_file)
    json_file.close()
    embed = discord.Embed(title="Bot Status", description="{}".format(data), color=discord.Color.red())
    await ctx.send(embed=embed)
