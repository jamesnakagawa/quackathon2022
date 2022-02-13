from client import client
from models import Session, Player, Battle

session = Session()

@client.command(name="challenge", help="Challenge another player to fight for breadcrumbs")
async def challenge(ctx):
  p1 = session.query(Player).filter(Player.handle == ctx.author.mention)
  if p1.count() == 0:
    p1 = Player(handle=ctx.author.mention)
    session.add(p1)
  p2 = session.query(Player).filter(Player.handle == ctx.subcommand_passed)
  if p2.count() == 0:
    if ctx.subcommand_passed in [user.mention for user in client.users]:
      p2 = Player(handle=ctx.subcommand_passed)
      session.add(p2)
    else:
      await ctx.send("Sorry, couldn't find that user.")
      return

  battle = Battle(player1=p1, player2=p2)

  p1_discord = next((user for user in client.users if user.mention == p1.handle), None)
  p2_discord = next((user for user in client.users if user.mention == p2.handle), None)

  await p2_discord.send(f"{ctx.author.mention} has challenged you to a battle. Do you accept? (Y/N)")

  session.commit()
