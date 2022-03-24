import discord
from discord import channel, guild
from discord import message
from discord.enums import ChannelType
from discord.utils import get
from discord.ext import tasks
import json
import requests
import asyncio
import time

bot = discord.Client()
arr = []

with open("./keys.json", "r") as file:
        data = json.load(file)
        TOKEN = data['token']
        print("Bot Running")

@bot.event
async def on_ready():
    channel2 = bot.get_channel(Channel_ID)
    await channel2.purge()
    channel = bot.get_channel({Channel_ID})
    await channel.purge()
    global status
    status = requests.get("https://api.whale-alert.io/v1/status?api_key=qKPYPcqsN8vlKWfxvpZai3aUqXMzZmsk").json()
    for i in status['blockchains']:
        if i['name'] == 'ripple':
            if str(i['status']) == "connected":
                emoji = "green_circle"
            else:
                emoji = "red_circle"
            stri = str("Status to the XRP and Whale Alert API: " + i['status'] + "   :" + emoji + ":")
            global message
            message = await channel.send(stri)


@tasks.loop(minutes=4.9)
async def background_task():
    await bot.wait_until_ready()
    await asyncio.sleep(2)
    for i in status['blockchains']:
        if i['name'] == 'ripple':
            if str(i['status']) == "connected":
                emoji = "green_circle"
            else:
                emoji = "red_circle"
            stri = str("Status to the API (Updated every 5 minutes): " + i['status'] + "   :" + emoji + ":")
            message.channel.purge(limit=1)
            await message.edit(content=stri)

@tasks.loop(seconds=5.7)
async def on_update():
    await bot.wait_until_ready()
    channel3 = bot.get_channel({Channel_ID})
    global data
    data = requests.get("https://api.whale-alert.io/v1/transactions?api_key=qKPYPcqsN8vlKWfxvpZai3aUqXMzZmsk").json()['transactions']
    for i in data:
        print(i)
        cal = time.strftime('[%Y-%m-%d] %H:%M:%S', time.localtime(i['timestamp']))
        for j in arr:
            if i['id'] in j['id']:
                return
            elif i['blockchain'] == "tron":
                return
        arr.append(i)
        print(i)
        if (i['amount_usd'] > 500000):
            if (str(i['blockchain'] == "ripple")):
                temp = 3447003
            if (str(i['blockchain'] == "bitcoin")):
                temp = 15105570
            if (str(i['blockchain'] == "ethereum")):
                temp = 9936031
            else:
                return
            embed1 = discord.Embed(
            title=str(cal),
            colour = discord.Colour(temp)
            #colour = discord.Colour(0x000000)
            )
            embed1.add_field(name = "Name: ", value = i['blockchain'], inline = False)
            embed1.add_field(name = "Transaction Type: ", value = i['transaction_type'], inline = False)
            try:
                embed1.add_field(name = "From: ", value = str("[" + i['from']['owner_type'] + " - " + i['from']['owner_type'] + "]"+ "  " + i['from']['address']), inline = False)
            except:
                embed1.add_field(name = "From: ", value = str("[" + i['from']['owner_type'] + "]"+ "  " + i['from']['address']), inline = False)
            try:
                embed1.add_field(name = "To: ", value = str("[" + i['to']['owner_type'] + " - " + i['from']['owner_type'] + "]" + "  " + i['to']['address']), inline = False)
            except:
                embed1.add_field(name = "To: ", i = str("[" + i['to']['owner_type'] + "]"+ "  " + i['to']['address']), inline = False)
            embed1.add_field(name = str("Amount [" + i['symbol'] + "]: "), value = i['amount'], inline=True)
            embed1.add_field(name = str("Amount [USD]: "), value = i['amount_usd'], inline=True)
            embed1.set_footer(text="Made by: Anon0x19#0001")
            embed1.set_author(name="Whale Alert")
            global message2
            message2 = await channel3.send(embed=embed1)


#@tasks.loop(seconds=86400)
#async def clear():
#    channel3 = bot.get_channel(844975733204975616)
#    channel3.purge(limit=1000)
    

#clear.start()
background_task.start()
on_update.start()

# @bot.event
# async def on_message(message_sent, message2):
#     if (message_sent.channel.id == 844975733204975616):
#         if (message_sent.content == message2):
#             message_sent.channel.purge(limit=-1)

bot.run(TOKEN)
