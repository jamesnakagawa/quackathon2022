from client import client
import json

# On message received

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "duck":
        await message.channel.send('Quack!')
    elif message.content == "status":
        await message.channel.send('Quackmon!')

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
