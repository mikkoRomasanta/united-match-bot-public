import asyncio
import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

import gcalendar
import mypath

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
ROLE_ID = os.getenv('DISCORD_ROLE_ID')
file_status = mypath.data_folder / "status.txt"

client = discord.Client()


def welcome():
    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
        print('running ping role task')
        next_match_ping.start()


def await_message_gg():
    print('Awaiting message(GG!)')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == 'GG!':
            response = 'MU!'
            await message.channel.send(response)

        if message.content == 'NEXT MATCH!':
            next_match = gcalendar.get_next_match()
            match_summary = next_match[0]
            match_time = next_match[1]
            response = f'{match_summary} || {match_time}'
            await message.channel.send(response)


@tasks.loop(minutes=30)
async def next_match_ping():  # pings the role 1hr+ before the next match
    time_bool = gcalendar.compare_time()
    if time_bool == True:
        next_match = gcalendar.get_next_match()
        match_summary = next_match[0]
        match_time = next_match[1]
        print(match_summary, match_time)

        # message for ping
        message = f"IT'S GAMEDAY! {match_summary} @ {match_time}"
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(f"<@&{ROLE_ID}> {message}")
        print('sent cron message')
        try:
            os.remove(file_status)
        except BaseException:
            exit('no status file found. exiting...')
        exit('Done')
    print(time_bool)


def run_client():
    client.run(TOKEN)


if __name__ == "__main__":
    welcome()
    await_message_gg()
    run_client()
