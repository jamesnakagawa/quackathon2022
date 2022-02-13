from client import client

@client.event
async def on_reaction_add(reaction, user):
    channel = client.get_channel(942101706739699735)
    await channel.send('Pinging {}'.format(user.mention) + ' has caught the duck!')