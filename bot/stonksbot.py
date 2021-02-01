import discord
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from yahoo_finance_async import OHLC, Interval, History

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$stonks'):
        while True:
            ticker = message.content.split('$stonks ',1)[1]
            await message.channel.send('Getting stonks, this may take some time...')
            result = await OHLC.fetch(ticker,interval=Interval.HOUR,history=History.DAY)
            price = str(result['meta']['regularMarketPrice'])
            await message.channel.send('TODAYS DATA FOR ' + ticker.upper() + '\nCurrent Stock Price: ' + price + '\nToday\'s High: ' + str(result['candles'][0]['high']) + '\nToday\'s Low: ' + str(result['candles'][0]['low']))
            break
        

client.run(TOKEN)
