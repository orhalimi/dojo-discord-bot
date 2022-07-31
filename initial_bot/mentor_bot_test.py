# bot.py
import pdb
import sys
import os
import random
import discord
import argparse
from discord.ext import commands
from discord.utils import get
from api import post_data, profile_exist, room_exist
from discord import ClientUser














def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', dest='token',
                        help="If you don't have the token please ask Eran to send it to you")
    parser.add_argument('-g', '--guild_name', dest='guild',
                        default="mentorbot_test")
    return parser.parse_args()

















def main():
    addrs = "http://127.0.0.1:8000"

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
    # @commands.has_role('room-creator')
    async def make_private_channel(ctx, *members: discord.Member):
        guild = ctx.guild

        overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
            }
            
        for member in members:
            overwrites[member] = discord.PermissionOverwrite(read_messages=True)
        
        room_name = f'{members[1].display_name}_mentors_{members[0].display_name}'
        
        existing_channels = discord.utils.get(guild.channels, name=room_name)


        if not existing_channels:
            members_str = ', '.join(m.name for m in members)
            channel = await guild.create_text_channel(room_name, overwrites=overwrites)
            channelId = channel.id



        room_path = f"http://127.0.0.1:8000/api/rooms/{channel.id}/"

        createRoom(channel.id)

        for i in range(len(members)):
            profile_path = f"http://127.0.0.1:8000/api/profiles/{members[i].id}/"
            role = f"http://127.0.0.1:8000/api/roles/{i+1}/"

            if profile_exist(members[i].id):
                createMember(profile_path, role, room_path)
            else:
                createProfile(id = members[i].id, name = members[i].display_name)
                createMember(profile_path, role, room_path)

        await ctx.send(f'Creating a private channel called {room_name} and adding {members_str} to it.')



    @bot.event
    async def on_message(ctx):
        if ctx.content.startswith('!'):
            pass
        else:
            content = ctx.content
            if ctx.author.id != 959437090070880286:
                # maybe we should add more section for discord id for message?
                if profile_exist(ctx.author.id) == False:
                    createProfile(ctx.author.id, ctx.author.display_name)

                if room_exist(ctx.channel.id) == False:
                    createRoom(ctx.channel.id)
                        
                profile_path = f"http://127.0.0.1:8000/api/profiles/{ctx.author.id}/"
                room_path = f"http://127.0.0.1:8000/api/rooms/{ctx.channel.id}/"
                createMessage(content, profile_path, room_path)

        await bot.process_commands(ctx)


    def createRoom(id: int):
        data = {"room_id": id}
        return post_data("rooms", data)


    def createProfile(id: int, name: str):
        profile_data = {
            "profile_id": id,
            "discord_name": name
        }
        return post_data("profiles", profile_data)
   

    def createMember(profile_path: str, role_path: str, room_path: str):
        member_data = {
            "profile": profile_path,
            "role": role_path,
            "room": room_path
        }
        return post_data("members", member_data)


    def createMessage(content: str, profile_path: str, room_path: str):
        message_data = {
            "content": content,
            "profile": profile_path,
            "room": room_path
        }
        return post_data("messages", message_data)
   

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


