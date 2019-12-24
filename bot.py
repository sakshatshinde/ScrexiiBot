import os, discord, webbrowser
from dotenv import load_dotenv
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

#Storing API keys safely.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()
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


@bot.command(name = "search")
async def search(ctx,*,arg):
    link = f'https://google.com/search?q={arg}/'
    #webbrowser.get().open(link.replace(" ",""))
    await ctx.send(link.replace(" ",""))

bot.run(TOKEN)