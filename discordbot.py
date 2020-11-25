import asyncio
import os

import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

import gcalendar
import mypath
import rds

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
ROLE_ID = os.getenv('DISCORD_ROLE_ID')
file_status = mypath.data_folder / "status.txt"

bot = commands.Bot(command_prefix='!')


def welcome():
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        print('running ping role task')
        next_match_ping.start()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!chelp for commands"))


def await_commands():
    print('Awaiting commands')

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error

    @bot.command()
    async def GG(ctx):
        await ctx.send('MU!')

    @bot.command()  # returns next match datetime + summary
    async def nmatch(ctx):  # next match
        next_match = gcalendar.get_next_match()
        match_summary = next_match[0]
        match_time = next_match[1]
        response = f'{match_summary} || {match_time}'
        await ctx.send(response)

    @bot.command()  # enable predictions for user
    async def pjoin(ctx):  # prediction join
        username = str(ctx.author)
        status = rds.register_user(username)
        if status == True:
            await ctx.send(f'{ctx.author} Registered!')
        else:
            await ctx.send(f'{ctx.author} is already registered!')

    @bot.command()  # end prediction time
    async def pend(ctx):  # prediction time end
        role = discord.utils.get(
            ctx.guild.roles,
            name="Di Bleck Pentha")  # change to admin role name
        if role in ctx.author.roles:
            response = rds.prediction_time_end()
            await ctx.send(response)
        else:
            await ctx.send('For Bleck Pentha Only!')

    @bot.command()  # force start prediction time
    async def pstart(ctx):  # prediction time start
        role = discord.utils.get(
            ctx.guild.roles,
            name="Di Bleck Pentha")  # change to admin role name
        if role in ctx.author.roles:
            date = gcalendar.get_current_time()
            response = rds.prediction_time_start(date)
            await ctx.send(response)
        else:
            await ctx.send('For Bleck Pentha Only!')

    @bot.command()
    async def pent(ctx, args):  # prediction enter
        username = str(ctx.author)
        print(username, args)
        response = rds.prediction_enter(username, args)
        await ctx.send(response)

    @bot.command()
    async def mend(ctx, args):  # match end
        role = discord.utils.get(
            ctx.guild.roles,
            name="Di Bleck Pentha")  # change to admin role name
        if role in ctx.author.roles:
            response = rds.end_match(args)
            await ctx.send(response)
        else:
            await ctx.send('For Bleck Pentha Only!')

    @bot.command()  # shows leaderboard
    async def sshow(ctx):  # score show
        response = rds.show_scores()
        await ctx.send(response)

    @bot.command()  # show current entries
    async def pshow(ctx):  # show predictions for the period
        response = rds.show_predictions()
        await ctx.send(response)

    @bot.command()  # show list of commands
    async def chelp(ctx):  # command help
        response = get_commands()
        await ctx.send(response)


@tasks.loop(minutes=30)  # 30
async def next_match_ping():  # pings the role 1hr+ before the next match
    time_bool = gcalendar.compare_time()
    if time_bool == True:
        next_match = gcalendar.get_next_match()
        match_summary = next_match[0]
        match_time = next_match[1]
        match_time2 = next_match[2]  # for database insertion
        print(match_summary, match_time)

        # message for ping
        message = f"IT'S GAMEDAY! {match_summary} @ {match_time}"
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"<@&{ROLE_ID}> {message}")
        print('sent cron message')

        await asyncio.sleep(3)

        response = rds.prediction_time_start(match_time2)
        await channel.send(response)

        # wait before looping again. This is to make sure only 1
        # message is sent
        await asyncio.sleep(4000)  # 4000
    print(time_bool)


def get_commands():
    response = '''----- COMMANDS ----- \n *use ! to access all commands*
        !nmatch \t| next match | get next match schedule
        !pjoin \t| prediction join \t| enables prediction on account
        !pent \t| prediction enter \t| enters your prediction [use the proper format]
        format:[W|L|D / score-score (utd score always on the right) ex. W/3-2 or L/1-4
        !pshow \t| prediction show \t| shows prediction from latest prediction period
        !sshow \t| score show \t| shows current leaderboard
        ----- FOR ADMIN ONLY -----
        \!pstart \t| prediction start \t| enables prediction time *is set on auto 1 hour before start of match*
        \!pend \t| prediction join \t| disables prediction time
        \!mend \t| match end \t| end the match and tally prediction scores'''

    return response


def run_bot():
    bot.run(TOKEN)


if __name__ == "__main__":
    welcome()
    # await_message_gg()
    await_commands()
    run_bot()
