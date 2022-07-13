# bot.py

import sys
import os
import random
from typing import Dict
import discord
import argparse
from discord.ext import commands
from discord.utils import get
import test_api as api 


url = "http://127.0.0.1:8000/api"

STUDENT_ROLE= f"{url}/roles/1/"
MENTOR_ROLE= f"{url}/roles/2/"
SUPER_MENTOR_ROLE= f"{url}/roles/3/"

def get_member_obj(id,role,channel) -> Dict :
    return {
        "role":role,
        "room" : f"{url}/rooms/{channel.id}/",
        "profile":f"{url}/profiles/{id}/",
        }


def create_overwrites(guild, members) :
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
            }
            for member in members:
                overwrites[member] = discord.PermissionOverwrite(
                read_messages=True)
            return overwrites     
          
def room_does_not_exist(guild, room_name) : 
            for channel in guild.channels: 
                if room_name == channel.name:
                    return False
            return True 

async def create_room(ctx,members,room_name,overwrites) :
            members_str = ', '.join(m.name for m in members)
            room_created_message = f'Creating a private channel called {room_name} and adding {members_str} to it.'
            channel = await ctx.guild.create_text_channel(room_name, overwrites=overwrites)
            add_room_to_db_and_update_members(channel,members)
            await ctx.send(room_created_message)

def add_room_to_db_and_update_members(channel,members):
    api.push_data("rooms",{"room_id": channel.id}) 
    for (member,role) in zip(members,[STUDENT_ROLE,MENTOR_ROLE,SUPER_MENTOR_ROLE]):
        api.push_data("profiles",{"profile_id": member.id,"discord_name":{str(member)}})
        api.push_data("members",get_member_obj(member.id,role,channel))


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

    
       
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')  
        

    @bot.command(name='private')
    # @commands.has_role('room-creator') ##Only server owner or someone with room-creator role can use this command;
    async def make_private_channel(ctx, *members: discord.Member):
        '''
        Takes a list of upto 3 members: A mentee, a mentor and a super mentor. Order of mentioned members is important.
        Creates a room with the name of the 2 first members in the format of: mentor mentors mentee.
        Creates an object to the db for the room and each of the members.
        '''

        overwrites = create_overwrites(ctx.guild,members)

        #Discord saves channel names in all lower case.
        room_name = f'{members[1].display_name}_mentors_{members[0].display_name}'.lower()
       
        if room_does_not_exist(ctx.guild, room_name):
          await create_room(ctx,members,room_name,overwrites)
        else:
            await ctx.send(f'A room with the name: {room_name} already exists. Please check if a room with these members already exists.')

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
