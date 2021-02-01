import yfinance as yf
import discord
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
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
            
            await message.channel.send('Getting stonks, this may take some time...')
            result = await OHLC.fetch('gme',interval=Interval.HOUR,history=History.DAY)
            price = str(si.get_live_price('gme'))
            await message.channel.send('TODAYS DATA FOR GME\nCurrent Stock Price: ' + price + '\nToday\'s High: ' + str(result['candles'][0]['high']) + '\nToday\'s Low: ' + str(result['candles'][0]['low']))
            break
        

client.run(TOKEN)
