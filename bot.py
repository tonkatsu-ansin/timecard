import discord
from discord.ext import commands
from datetime import datetime,timedelta,timezone
from os import getenv

bot = commands.Bot(command_prefix='$')

def get_destination():
    Channel = bot.get_channel(int(getenv('CHANNEL_ID')))
    return Channel

@bot.event
async def on_ready():
    destination = get_destination()
    await destination.send("Timecard is ready!")

@bot.event
async def on_voice_state_update(Member,before,after):
    if (before.channel != after.channel) and Member.name != bot.user.name:
        destination = get_destination()
        now = datetime.now(timezone(timedelta(hours=9)))
        date = str(now.strftime("%Y/%m/%d %H:%M:%S")+" ")

        if(before.channel is None): 
            await destination.send(date + Member.name + " joined to " + str(after.channel))
        elif(after.channel is None):
            await destination.send(date + Member.name + " left " + str(before.channel))
        elif(after.channel != before.channel):
            await destination.send(date + Member.name + " moved to " + str(after.channel) + " from " + str(before.channel))

@bot.event
async def on_command_error(ctx,error):
    pass #botのpingのクールダウン中にカスタムステータスに設定したい

@bot.command()
@commands.cooldown(1,180,commands.BucketType.channel)
async def ping(ctx):
    await ctx.send("pong")

bot.run(getenv('BOT_TOKEN'))