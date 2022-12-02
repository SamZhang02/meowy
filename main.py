# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv 
import os 
from pathlib import Path

#Get bot key from .env
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        if message.author == 'wugway#7417':
            await message.channel.send('tg simon')
        else:
            await message.channel.send('I am Ally\'s unfinished project bot')
    
    if message.content == ('test image'):
        await message.channel.send('https://ichef.bbci.co.uk/news/976/cpsprodpb/16620/production/_91408619_55df76d5-2245-41c1-8031-07a4da3f313f.jpg')

client.run(TOKEN)
