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

# On message received
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  user = getuser(message.author.name)
  if user == None:
    user = Player(handle=message.author.name)
    session.add(user)
  p2_battle = user.current_battle_p2

  if p2_battle != None:
    if message.content.lower() in ['y', 'yes']:
      p2_battle.accepted = True
      await getdiscorduser(p2_battle.player1.handle).send(f"{message.author.name} has accepted your challenge!\n\nWhat would you like to do?\n1) Attack")

    elif message.content.lower() in ['n', 'no']:
      session.delete(p2_battle)
    else:
      await message.channel.send("Sorry, didn't understand you")

  p1_battle = user.current_battle_p1
  battle = None

  if p1_battle is not None and p1_battle.is_my_turn(user):
    battle = p1_battle
  if p2_battle is not None and p2_battle.is_my_turn(user):
    battle = p2_battle

  if battle is not None:
    if message.content.lower() in ['1']:
      still_going = p1_battle.do_turn(1)
      attacker = getdiscorduser(battle.attackerPlayer().handle)
      defender = getdiscorduser(battle.defenderPlayer().handle)
      if not still_going:
        await attacker.send(f"Aw yiss! You get all the breadcrumbs.")
        await defender.send(f"You lost. Damn")
      else:
        duck_name = battle.defender().nickname
        remaining_hp = battle.defender().current_hp
        await defender.send(f"{duck_name} got walloped and has {remaining_hp} HP left.\n\nWhat would you like to do?\n1) Attack")
    else:
      await message.channel.send("Sorry, didn't understand you")

  session.commit()
  await client.process_commands(message)
