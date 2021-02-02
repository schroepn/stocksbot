import discord
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from yahoo_finance_async import OHLC, Interval, History, api

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
        try:
        
            #gets the ticker from the input
            ticker = message.content.split('$stonks ',1)[1]
            #sends message saying it will take time so peopel don't get angery, also to tell user that bot has been called
            noticeEmbed = discord.Embed(title='Getting Stonks', description='this may take some time')
            sentMessage = await message.channel.send(embed=noticeEmbed)
            #gets the ticker data using yahoo_finance_async, data is every 15 minutes for the past day
            result = await OHLC.fetch(ticker,interval=Interval.DAY,history=History.DAY)
            print('got the ticker data')
            #gets the current price for a share
            price = result['meta']['regularMarketPrice']
            print('got the price at: ' + str(price))
            print('day price is: ' + str(result['meta']['regularMarketPrice']))
            #formats the message into an embed
            stonkInfoEmbed = discord.Embed(title='Today\'s Data for {stock}'.format(stock=ticker))
            stonkInfoEmbed.add_field(name='Current Price:',value='{pps:.3f}'.format(pps=price))
            stonkInfoEmbed.add_field(name='Today\'s High:',value='{high:.3f}'.format(high=result['candles'][0]['high']))
            stonkInfoEmbed.add_field(name='Today\'s Low:',value='{low:.3f}'.format(low=result['candles'][0]['low']))
            #sends the message to discord
            await sentMessage.edit(embed=stonkInfoEmbed)
        except api.APIError:
            await message.channel.send('ERROR: NSS (NO SUCH STOCK)')
        
        

client.run(TOKEN)
