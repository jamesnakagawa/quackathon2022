from client import client, session
from models import Player
id = 0

@client.event
async def on_reaction_add(reaction, user):
  #client.get_channel(942101706739699735)
  if user.bot == False and reaction.count <= 2:
    await reaction.message.channel.send('{}'.format(user.mention) + ' has caught the duck!')
    # user_db_entry = session.query(Player).filter(Player.handle == user.name).one_or_none()
    id = user.id
