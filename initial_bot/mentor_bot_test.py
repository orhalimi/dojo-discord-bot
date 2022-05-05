# bot.py
import pdb
import sys
import os
import random
import discord
import argparse
from datetime import datetime
from discord.ext import commands
from discord.utils import get


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', dest='token',
                        help="If you don't have the token please ask Eran to send it to you")
    parser.add_argument('-g', '--guild_name', dest='guild',
                        default="mentorbot_test")
    return parser.parse_args()


def main():
    parsed_args = parse_arguments()
    if parsed_args.token == None:
        print("Please try again, but this time enter a token as an argument")
        sys.exit()

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = '!', intents = intents, case_insensitive=True)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.command(name='private')
    # @commands.has_role('admin')
    async def make_private_channel(ctx, room_name, *members: discord.Member,):
        '''
        Takes 2 parameters: A room name and a list of tagged members to be added to the room.
        Creates a private room with the room name and addes the members to that room.
        Room name must not already exist in the server.
        '''

        if room_name == None:
            await ctx.send(f'Room name is empty, please add a room name to the command (after the last member to the be added to the room')
            return
        else:
            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
            }
            member_list = []
            for member in members:
                member_list.append(member.name)
                overwrites[member] = discord.PermissionOverwrite(
                    read_messages=True)

            existing_channels = discord.utils.get(
                guild.channels, name=room_name)
            if not existing_channels:
                members_names = (',').join(member_list)
                channel = await guild.create_text_channel(room_name, overwrites=overwrites)
                await ctx.send(f'Creating a private channel called {room_name} and adding {members_names} to it.')
            else:
                await ctx.send(f'A room with the name: {room_name} already exists. Please choose a different name.')


    # Send a gretting to members upon joining the server
    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    # Save messages that were sent in private mentoring rooms
    @bot.event
    async def on_message(message):
        '''        
        private mentoring rooms will have some identifier in their names, so the bot can decide whether or not to save the message.
        For now I am tentatively using "shlomi" as the identifier :-)
        
        '''
        prvt_ment_channels_mark = 'shlomi'
        channel = message.channel
        author = message.author
        if not author.bot and prvt_ment_channels_mark in channel.name:
            with open(f"initial_bot/{channel.name}_messages.txt", 'a+') as f:
                date = (message.created_at)
                f.write(f'{date:%d/%m/%Y %H:%M}\n{author.name}\n')
                f.write(message.content + "\n\n")
            bot.dispatch('documentation', channel, author.name)
    
    @bot.event
    async def on_documentation(channel, author):
       embed = discord.Embed(title="Message Documentation", description=f"{author} - your message has been saved", color=discord.Color.blurple()) # Let's make an embed!
       await channel.send(embed=embed)

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

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

    bot.run(parsed_args.token)


if __name__ == "__main__":
    main()
