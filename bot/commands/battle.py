from client import client, session
from models import Player, Battle, SpecificDuck, DuckType
from lib import duckmon

def getuser(name):
  user = session.query(Player).filter(Player.handle == name).one_or_none()
  return user

def getdiscorduser(name):
  return next((user for user in client.users if user.name == name), None)

@client.command(name="challenge", help="Challenge another player to fight for breadcrumbs")
async def challenge(ctx):
  subcommand = ctx.message.content.split(' ')[1]
  p1 = getuser(ctx.author.name)
  if p1 == None:
    p1 = Player(handle=ctx.author.name)
    session.add(p1)
  p2 = getuser(subcommand)
  if p2 == None:
    if subcommand in [user.name for user in client.users]:
      p2 = Player(handle=subcommand)
      session.add(p2)
    else:
      await ctx.send("Sorry, couldn't find that user.")
      return

  _, mood, attack, defend, *rest = duckmon.get_specific_duck()
  d1_type = DuckType(name='type 1', description=mood, attack_coeff=attack, defend_coeff=defend)
  d1 = SpecificDuck(nickname=f"{ctx.author.name}'s duck", duck_type=d1_type)
  _, mood, attack, defend, *rest = duckmon.get_specific_duck()
  d2_type = DuckType(name='type 2', description=mood, attack_coeff=attack, defend_coeff=defend)
  d2 = SpecificDuck(nickname=f"{subcommand}'s duck", duck_type=d2_type)
  battle = Battle(player1=p1, player2=p2, duck1=d1, duck2=d2)

  session.add_all([d1_type, d1, d2_type, d2, battle])

  p1_discord = getdiscorduser(p1.handle)
  p2_discord = getdiscorduser(p2.handle)

  await p2_discord.send(f"{ctx.author.name} has challenged you to a battle. Do you accept? (Y/N)")

  session.commit()
