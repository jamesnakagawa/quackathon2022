from client import *
import asyncio
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@client.command(name='play', help='To play song')
async def play(ctx, *args):
    await join(ctx)

    print(len(args))
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            if (len(args) > 0):
                filename = await YTDLSource.from_url(args[0], loop=client.loop)
            else:
                filename = "The_Duck_Song-MtN1YnoL46Q.m4a"
            voice_channel.play(discord.FFmpegPCMAudio(
                executable='ffmpeg', source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
        ctx.send("Let the quacking commence!")
    except:
        await ctx.send("The duck is not connected to a voice channel.")


@client.command(name='join', help='Tells the duck to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.mention))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@client.command(name='leave', help='To make the duck leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The duck is not connected to a voice channel.")


@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Not quacking at the moment.")


@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Unable to stop quacking.")


@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.send("Quacking stopped!")
    else:
        await ctx.send("Not quacking at the moment.")
