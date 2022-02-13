from turtle import clear
from client import client

@client.event
async def on_reaction_add(reaction, user):
    channel = client.get_channel(942101706739699735)
    check = 0
    #reaction.message.author
    if user.bot == False:
        await channel.send('{}'.format(user.mention) + ' has caught the duck!')
