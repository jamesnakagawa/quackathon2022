from client import client

@client.event
async def on_reaction_add(reaction, user):
    #client.get_channel(942101706739699735)
    if user.bot == False and reaction.count <= 2:
        await reaction.message.channel.send('{}'.format(user.mention) + ' has caught the duck!')
