import os, discord, webbrowser
from dotenv import load_dotenv
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import youtube_dl
from discord.utils import get

#Storing API keys safely.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", description='A discord bot which can listen to your rambling')

@bot.event
async def on_ready():
    print(f'{bot.user.name} connection established to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("with 💬👂"))

@bot.event   #sending a welcome msg via dm
async def on_member_join(member):
    await member.create_dm()    
    await member.dm_channel.send(
        f'Hieee {member.name}, welcome to my Discord server!'
    )

@bot.command(pass_context = True, name = "kick")    #kick
@commands.has_permissions(kick_members = True)  
async def kick(ctx, member : discord.Member,*,reason = None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')
    except:
        await ctx.send('Something went wrong')

@bot.command(pass_context = True, name = "ban")     #ban
@commands.has_permissions(ban_members = True) 
async def ban(ctx, member : discord.Member, *, reason = None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    except:
        await ctx.send('Something went wrong')


@bot.command(name = "search")                       #google search
async def search(ctx,*,arg):
    link = f'https://google.com/search?q={arg}/'
    #webbrowser.get().open(link.replace(" ",""))
    await ctx.send(link.replace(" ",""))

@bot.command(name = "info")
async def info(ctx):
    embed = discord.Embed(title="Screxii Bot", description="A discord bot which can talk", colour=discord.Color.dark_teal())
    #embed.set_author(name="ScreX", icon_url=bot.user.avatar_url)
    embed.set_footer(text="Made by ScreX", icon_url=ctx.author.avatar_url)
    embed.set_image(url='https://discordpy.readthedocs.io/en/latest/_images/snake.png')
    embed.set_thumbnail(url='https://www.python.org/static/img/python-logo.png')
    await  ctx.send(embed = embed)

@bot.command(name = "ping")     #latency check
async def ping(ctx):
	await ctx.send(f'Pong 🏓 {round(bot.latency * 1000)}ms')

#------------------------------------AUDIO------------------------------------#
@bot.command(name = "join")
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except:
        await ctx.send('You might want to join a VC first dummy')

@bot.command(name = "leave")
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
    except:
        pass

@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except:
        await ctx.send('You might want to join a VC first dummy')

    song_there = os.path.isfile("song.mp3")

    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!")) #playing the song
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.80      #volume

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

#------------------------------------AUDIO END------------------------------------#

bot.run(TOKEN)