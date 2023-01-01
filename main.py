import logging
import os
from pathlib import Path

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import database
import daytime
from commands import run_command
from market_info import get_major_index

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Logging starts here')

#Get bot key from .env
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler(timezone='America/Toronto')

@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user}')
    logging.info(f'Logged in as {client.user}')
    if not os.path.exists('database.db'):
        database.create_db()

    # TODO: Check if there is currently a scheduler -> check if there are any expired jobs in scheduled jobs 

    next_close = daytime.get_next_close()

    notify_is_scheduled = False 

    for job in scheduler.get_jobs():
        if job.name == 'notify':
            notify_is_scheduled = True

    if not notify_is_scheduled:
        scheduler.add_job(notify, 'date', args=[scheduler],run_date = next_close, misfire_grace_time=None)
        scheduler.start()

    logging.info(scheduler.get_jobs())
    print(f'Next market notification scheduled for {next_close}')
    logging.info(f'Next market notification scheduled for {next_close}')

@client.event
async def on_resumed() -> None:
    print('Resumed')
    logging.info(f'Resumed')

@client.event
async def on_message(message:discord.Message) -> None:
    if message.author == client.user:
        return
    
    if message.content.startswith('stonk'):
        try:
            await run_command(message)
            await message.add_reaction('✅')
        except Exception as e:
            await message.add_reaction('❌')
            await message.channel.send(e)

async def notify(scheduler) -> None:
    channels = database.get_channels_to_notify()
    logging.info(channels)
    market = get_major_index(f'Market Close - {daytime.today_date()}') 
    logging.info(market.quotes)
    for channel_id in channels:
        channel = client.get_channel(channel_id)
        try:
            await channel.send(embed=market.get_embed())
        except Exception as e:
            logging.error(e)

    next_close = daytime.get_next_close()
    scheduler.add_job(notify, 'date', args=[scheduler],run_date=next_close, misfire_grace_time=None)

    scheduler.print_jobs()
    print(f'Next market notification scheduled for {next_close}')
    logging.info(f'Next market notification scheduled for {next_close}')

client.run(TOKEN) # type: ignore
