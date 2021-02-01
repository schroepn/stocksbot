import yfinance as yf
import discord
import pandas as pd
import numpy as np
import json
from yahoo_fin import stock_info as si
from dotenv import load_dotenv
import os

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
            try:
                await message.channel.send('Getting stonks, this may take some time...')
                ticker = message.content.split('$stonks ',1)[1]
                print(ticker)
                stonk = yf.Ticker(ticker)
                # get stock info
                df = stonk.history(period="1d")
                print(df.index)
                price = str(si.get_live_price(ticker))
                await message.channel.send('TODAYS DATA FOR ' + ticker.upper() + '\nCurrent Stock Price: ' + price + '\nToday\'s High: ' + np.array2string(df.iat[1,2]) + '\nToday\'s Low: ' + np.array2string(df.iat[1,3]))
                break
            except Exception:
                await message.channel.send('oopsie woopsie, we fucky wuckied! either twy again or dewete bot OwO')
                break
        

client.run(TOKEN)
