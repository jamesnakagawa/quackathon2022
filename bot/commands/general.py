from client import client

# On start

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def shutdown(ctx):
    client.logout()
    client.close()
    exit()
