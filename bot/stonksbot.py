import discord
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from yahoo_finance_async import OHLC, Interval, History, api
import atexit

print(os.getcwd())
print(os.listdir())
os.chdir('./bot')
print(os.getcwd())
print(os.listdir())
tokenFile = open('token.txt', 'r')
TOKEN = tokenFile.read()
#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

client = discord.Client()


@bot.event
async def on_ready():
    print('Beep Boop Bot Is On...'.format(client))

@bot.command()
async def stonks(ctx, ticker):
    if ctx.author.bot:
        return
    #sends message saying it will take time so peopel don't get angery, also to tell user that bot has been called
    noticeEmbed = discord.Embed(title='Getting Stonks', description='this may take some time')
    sentMessage = await ctx.send(embed=noticeEmbed)
    try:
        #gets the ticker data using yahoo_finance_async, data is the overview of the last trading day
        result = await OHLC.fetch(ticker,interval=Interval.DAY,history=History.DAY)
        
        #gets the current price for a share
        price = result['meta']['regularMarketPrice']
        
        #formats the message into an embed
        stonkInfoEmbed = discord.Embed(title='Today\'s Data for {stock}'.format(stock=ticker),color=0xf812ec)
        stonkInfoEmbed.add_field(name='Current Price:',value='{pps:.3f}'.format(pps=price),inline=False)
        stonkInfoEmbed.add_field(name='Today\'s High:',value='{high:.3f}'.format(high=result['candles'][0]['high']),inline=False)
        stonkInfoEmbed.add_field(name='Today\'s Low:',value='{low:.3f}'.format(low=result['candles'][0]['low']),inline=False)
        
        #sends the message to discord
        await sentMessage.edit(embed=stonkInfoEmbed)
    except api.APIError:
        errorEmbed = discord.Embed(title='ERROR: NSS',description='NO SUCH STOCK',color=0xf812ec)
        await sentMessage.edit(embed=errorEmbed)

@bot.command()
async def sar(ctx):
    if ctx.author.bot:
        return
    await ctx.send('Sarukei Is Not Cool')


@bot.command()
async def kill(ctx):
    if ctx.author.id == 200802901944303616:
        await ctx.send('I am kill')
        await cleanup()
        quit()



async def cleanup():
    print ('committing seppuku')
    await bot.logout()

atexit.register(cleanup)


bot.run(TOKEN)
