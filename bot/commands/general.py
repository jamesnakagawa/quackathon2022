from client import client

# On start

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(942101706739699735)
    await channel.send('BOT ACTIVE')


@client.command()
async def shutdown(ctx):
    client.logout()
    client.close()
    exit()
