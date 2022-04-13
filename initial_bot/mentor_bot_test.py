# bot.py
import sys
import os
import random
import discord
import argparse
from discord.ext import commands

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', dest = 'token', help = "If you don't have the token please ask Eran to send it to you")
    parser.add_argument('-g', '--guild_name', dest = 'guild', default = "mentorbot_test")
    return parser.parse_args()

def main():
    parsed_args = parse_arguments()
    if parsed_args.token == None:
        print("Please try again, but this time enter a token as an argument")
        sys.exit()

    intents = discord.Intents.all()
    discord.member = True
    bot = commands.Bot(command_prefix='!', intents = intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    # Send a gretting to members upon joining the server
    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    # Reply to a !99 message with a random Peralta quote
    @bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
    async def nine_nine(ctx):
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    # A !roll_dice message should be accompanied with 2 numbers - the 1st for the number of dice and the 2nd for the number of sides each die has
    # Roll the dice and return the sum of random numvers received
    @bot.command(name='roll_dice', help='Simulates rolling dice.')
    async def roll(ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    # Create a new channel in the server
    # The channel's name is received by the caller as an argument
    # The caller must have an admin role
    @bot.command(name='create-channel')
    @commands.has_role('admin')
    async def create_channel(ctx, channel_name = None):
        if channel_name == None:
            await ctx.send("Please add the channel name as an argument")
        else:
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if not existing_channel:
                await ctx.send(f'Creating a new channel: {channel_name}')
                await guild.create_text_channel(channel_name)

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

    bot.run(parsed_args.token)

if __name__ == "__main__":
  main()