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
        
        #gets the ticker from the input
        ticker = message.content.split('$stonks ',1)[1]
        #sends message saying it will take time so peopel don't get angery
        await message.channel.send('Getting stonks, this may take some time...')
        #gets the ticker data using yahoo_finance_async, data is every 15 minutes for the past day
        result = await OHLC.fetch(ticker,interval=Interval.DAY,history=History.DAY)
        dayprice = await OHLC.fetch(ticker,interval=Interval.MINUTE,history=History.DAY)
        print('got the ticker data')
        #gets the current price for a share
        price = dayprice['meta']['regularMarketPrice']
        print('got the price at: ' + str(price))
        print('day price is: ' + str(result['meta']['regularMarketPrice']))
        #formats the message
        toSend = 'Today\'s Data for {stock}\nCurrent Stock Price: {pps:.3f}\nToday\'s High: {high:.3f}\nToday\'s Low: {low:.3f}'
        #sends the message to discord
        await message.channel.send(toSend.format(stock=ticker,pps=price,high=result['candles'][0]['high'],low=result['candles'][0]['low']))
        
        

client.run(TOKEN)
