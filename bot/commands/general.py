from client import client, discord

# On start


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Gotta quack em all!'))
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def shutdown(ctx):
    client.logout()
    client.close()
    exit()
