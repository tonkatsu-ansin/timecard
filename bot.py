import discord
from datetime import datetime,timedelta,timezone
from os import getenv

client = discord.Client()

def get_destination():
    Channel = client.get_channel(int(getenv('CHANNEL_ID')))
    return Channel

@client.event
async def on_ready():
    destination = get_destination()
    await destination.send("Timecard is ready!")

@client.event
async def on_voice_state_update(Member,before,after):
    if (before.channel != after.channel) and Member.name != client.user.name:
        destination = get_destination()
        now = datetime.now(timezone(timedelta(hours=9)))
        date = str(now.strftime("%Y/%m/%d %H:%M:%S")+" ")

        if(before.channel is None): 
            await destination.send(date + Member.name + " joined to " + str(after.channel))
        elif(after.channel is None):
            await destination.send(date + Member.name + " left " + str(before.channel))
        elif(after.channel != before.channel):
            await destination.send(date + Member.name + " moved to " + str(after.channel) + " from " + str(before.channel))

client.run(getenv('BOT_TOKEN'));