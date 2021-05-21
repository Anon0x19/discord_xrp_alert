import discord
from discord import channel, guild
from discord import message
from discord.utils import get
from discord.ext import tasks
import json
import requests
import asyncio
import time

bot = discord.Client()

with open("./keys.json", "r") as file:
        data = json.load(file)
        TOKEN = data['token']
        print("Bot Running")

@bot.event
async def on_ready():
    channel2 = bot.get_channel(844975733204975616)
    await channel2.purge()
    channel = bot.get_channel(844975691408736306)
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
            await message.edit(content=stri)

@tasks.loop(seconds=6.7)
async def on_update():
    await bot.wait_until_ready()
    await asyncio.sleep(0.1)
    channel3 = bot.get_channel(844975733204975616)
    try:
        global data
        data = requests.get("https://api.whale-alert.io/v1/transactions?api_key=qKPYPcqsN8vlKWfxvpZai3aUqXMzZmsk").json()['transactions'][0]
        # if data[-1]['blockchain'] == 'ripple':
        #     if data['symbol'] == 'xrp':
        if (data['amount_usd'] > 500000) and (data['blockchain'] == 'ripple'):
            cal = time.strftime('[%Y-%m-%d] %H:%M:%S', time.localtime(data['timestamp']))
            embed1 = discord.Embed(
            title=str(cal),
            colour = discord.Colour(0x000000)
            )
            embed1.add_field(name = "Name: ", value = data['blockchain'], inline = False)
            embed1.add_field(name = "Transaction Type: ", value = data['transaction_type'], inline = False)
            embed1.add_field(name = "From: ", value = str("[" + data['from']['owner_type'] + "]"+ "  " + data['from']['address']), inline = False)
            embed1.add_field(name = "To: ", value = str("[" + data['to']['owner_type'] + "]"+ "  " + data['to']['address']), inline = False)
            embed1.add_field(name = str("Amount [" + data['symbol'] + "]: "), value = data['amount'], inline=True)
            embed1.add_field(name = str("Amount [USD]: "), value = data['amount_usd'], inline=True)
            embed1.set_footer(text="Made by: Anon0x19#0001")
            embed1.set_author(name="Whale Alert")
            # temp = channel.last_message
            global message2
            message2 = await channel3.send(embed=embed1)
    except:
        return

# @bot.event
# async def on_message(message):
#     channel3 = bot.get_channel(844975733204975616)
#     if (message.channel == channel3) and (message.content == message2):
#         await message.purge(amount=1)

background_task.start()
on_update.start()

bot.run(TOKEN)