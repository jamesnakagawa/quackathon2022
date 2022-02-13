from client import client, session
from models import Player
import json

def getuser(name):
  user = session.query(Player).filter(Player.handle == name).one_or_none()
  return user

def getdiscorduser(name):
  return next((user for user in client.users if user.name == name), None)

# On message received

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content == "duck":
    await message.channel.send('Quack!')
  elif message.content == "status":
    await message.channel.send('Quackmon!')

  user = getuser(message.author.name)
  if user == None:
    user = Player(handle=message.author.name)
    session.add(user)

  p1_battle = user.current_battle_p1
  p2_battle = user.current_battle_p2

  if p2_battle != None and p2_battle.accepted == False:
    if message.content.lower() in ['y', 'yes']:
      p2_battle.accepted = True
      await getdiscorduser(p2_battle.player1.handle).send(f"{message.author.name} has accepted your challenge!\n\nWhat would you like to do?\n1) Attack")

    elif message.content.lower() in ['n', 'no']:
      session.delete(p2_battle)
  else:
    battle = None

    if p1_battle is not None and p1_battle.is_my_turn(user):
      battle = p1_battle
    elif p2_battle is not None and p2_battle.is_my_turn(user):
      battle = p2_battle

    if battle is not None:
      if message.content.lower() in ['1']:
        attacker = getdiscorduser(battle.attackerPlayer().handle)
        attack_duck_name = battle.attacker().nickname
        defender = getdiscorduser(battle.defenderPlayer().handle)
        defend_duck_name = battle.defender().nickname

        # turn switches as soon as this is called
        result = battle.do_turn(1)
        if result == False:
          xp, level_up = battle.win(user)
          await attacker.send(f"Aw yiss! You get all the breadcrumbs.\n{attack_duck_name} ate up {int(xp)} breadcrumbs. Nom nom nom")
          if level_up > 0:
            await attacker.send(f"Holey guacamoley! {attack_duck_name} leveled up!")
          await defender.send(f"You lost. Damn")
        else:
          damage, remaining_hp = result
          await attacker.send(f"{attack_duck_name} attacked for {int(damage)} points! {defend_duck_name} has {int(remaining_hp)} HP left.\nWaiting for your opponent to make a move...")
          await defender.send(f"{defend_duck_name} got walloped and has {int(remaining_hp)} HP left.\n\nWhat would you like to do?\n1) Attack")
      else:
        print('test1')


  session.commit()
  await client.process_commands(message)

  json_file = open('bot/settings.json', 'r', encoding="utf-8")
  data = json.load(json_file)
  json_file.close()

  msg_to_spawn = data['msg_to_spawn']
  curr_to_spawn = data['curr_to_spawn']

  curr_to_spawn += 1

  if (curr_to_spawn == msg_to_spawn):
    curr_to_spawn = 0
    from commands import quacks
    ctx = await client.get_context(message)
    await quacks.spawnFunc(ctx)

  data['curr_to_spawn'] = curr_to_spawn

  json_file = open('bot/settings.json', 'w', encoding="utf-8")
  json.dump(data, json_file)
  json_file.close()
