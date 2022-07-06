# bot.py
import pdb
import sys
import os
import random
from typing import Dict
import discord
import argparse
from discord.ext import commands
from discord.utils import get
import test_api as api 


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
    bot = commands.Bot(command_prefix = '!', intents = intents)

    roles = {
            'Student': "http://127.0.0.1:8000/api/roles/1",
            'Mentor': "http://127.0.0.1:8000/api/roles/2",
            'Super_Mentor': "http://127.0.0.1:8000/api/roles/3",
            }

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')  
        

    @bot.command(name='private')
    @commands.has_role('room-creator') ##Only server owner or someone with room-creator role can use this command;
    async def make_private_channel(ctx, *members: discord.Member):
        '''
        Takes a list of 3 members: A mentee, a mentor and a super mentor. Order of mentioned members is important.
        '''

        guild = ctx.guild
        overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
            }

        url = "http://127.0.0.1:8000/api"
        student = {
            "id": members[0].id,
            "name": members[0].display_name,
            "role": f"{url}/roles/1/"
        }
        mentor = {
            "id": members[1].id,
            "name": members[1].display_name,
            "role": f"{url}/roles/2/"
        }
        super_mentor = {
            "id": members[2].id,
            "name": members[2].display_name,
            "role": f"{url}/roles/3/"
        }

        def getMemberObj(member) -> Dict :
            return {
            "role":{member["role"]},
            "room" : f"{url}/rooms/{channel.id}/"
            ,"profile":f"{url}/profiles/{member['id']}/"
        }
            ## Creates the permissions to view the room about to be created.
        for member in members:
            overwrites[member] = discord.PermissionOverwrite(
                read_messages=True)

        room_name = f'{mentor["name"]}_mentors_{student["name"]}'
        existing_channels = discord.utils.get(
            guild.channels, name=room_name)
        if not existing_channels:
            members_str = ', '.join(m.name for m in members)
            channel = await guild.create_text_channel(room_name, overwrites=overwrites)
            api.push_data("rooms",{"room_id": channel.id})

            for member in members:
                api.push_data("profiles",{"profile_id": member.id,"discord_name":member.display_name})

            for member in [student,mentor,super_mentor]:
                api.push_data("members",getMemberObj(member))

            await ctx.send(f'Creating a private channel called {room_name} and adding {members_str} to it.')
        else:
            await ctx.send(f'A room with the name: {room_name} already exists. Please check if this room already exists.')

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

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

    bot.run(parsed_args.token)


if __name__ == "__main__":
    main()
