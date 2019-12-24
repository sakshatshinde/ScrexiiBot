import os, discord
from dotenv import load_dotenv
from discord.ext import commands

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

bot.run(TOKEN)