from client import client, discord

# On start


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Gotta quack em all!'))
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(942101706739699735)
    await channel.send('BOT ACTIVE')


@client.command()
async def shutdown(ctx):
    channel = client.get_channel(942101706739699735)
    await channel.send('BOT SHUTDOWN')
    client.logout()
    client.close()
    exit()
