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

    json_file = open('settings.json', 'w+', encoding="utf-8")
    data = json.loads(json_file)
    json_file.close()

