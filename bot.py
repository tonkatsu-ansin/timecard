import discord
from discord.ext import commands
from discord.utils import escape_markdown
from datetime import datetime,timedelta,timezone
from os import getenv

intents = discord.Intents.default()
bot = commands.Bot(intents=intents,command_prefix='\\')

def get_destination():
    Channel = bot.get_channel(int(getenv('CHANNEL_ID')))
    return Channel

@bot.event
async def on_ready():
    print('bot is ready')

@bot.event
async def on_voice_state_update(Member,before,after):
    if (before.channel != after.channel) and Member.name != bot.user.name:
        destination = get_destination()
        now = datetime.now(timezone(timedelta(hours=9)))
        date = str(now.strftime("%Y/%m/%d %H:%M:%S")+" ")
        if(before.channel is None): 
            await destination.send(escape_markdown(f'{date} {Member.name} joined to {str(after.channel)}'))
        elif(after.channel is None):
            await destination.send(escape_markdown(f'{date} {Member.name} left {str(before.channel)}'))
        elif(after.channel != before.channel):
            await destination.send(escape_markdown(f'{date} {Member.name} moved to {str(after.channel)} from {str(before.channel)}'))

bot.run(getenv('BOT_TOKEN'))