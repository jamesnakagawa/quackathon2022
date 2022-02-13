from client import client
import json
# bot commands


@client.command(name="spawnfrequency", help="Changes the spawn frequency of ducks")
async def ducky(ctx, arg):

    try:
        num = int(arg)

        json_file = open('bot/settings.json', 'r', encoding="utf-8")
        data = json.load(json_file)
        json_file.close()

        data['msg_to_spawn'] = num
        data['curr_to_spawn'] = 0

        json_file = open('bot/settings.json', 'w', encoding="utf-8")
        json.dump(data, json_file)
        json_file.close()

        await ctx.channel.send("Spawn frequency is now: {}".format(num))
    except Exception as e:
        await ctx.channel.send("EXCEPTION: {}".format(str(e)))
