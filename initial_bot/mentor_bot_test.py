# bot.py
import os
import random
from re import S
import discord
import argparse
from discord.ext import commands

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', dest = 'token', help = "If you don't have the token please ask Eran to send it to you")
    parser.add_argument('-g', '--guild_name', dest = 'guild', default = "Dojo bots lab")
    
    return parser.parse_args()

parsed_args = parse_arguments()




bot = commands.Bot(command_prefix='!')





@bot.event
async def on_ready():   
    
    for guild in bot.guilds:
      print(bot.guilds[0])
      print(guild.users)
      guild = (bot.guilds[0])
    print(f'{bot.user.name} has connected to Discord!')

# async def create_new_channel(ctx, *, room_name):
#     print(f'Confirmed')
#     guild = ctx.guild
#     role=room_name
#     # await ctx.send(role)
#     # autorize_role = await guild.create_role(name=role)
#     # overwrites = {
#     #     guild.default_role: discord.PermissionOverwrite(read_messages=False),
#     #     guild.me: discord.PermissionOverwrite(read_messages=True),
#     #     autorize_role: discord.PermissionOverwrite(read_messages=True)
#     # }
#     await guild.create_text_channel(room_name)
#     # await ctx.author.add_roles(autorize_role) 
#     print(f'Creating a new channel: {room_name}')
#     await ctx.send(f'Created room: {room_name}')
        


    






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

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='create-channel')
# @commands.has_role('admin')
async def create_channel(ctx, channel_name='shlomi_test'):
    guild = ctx.guild
    print(guild)
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel: 
        await ctx.send('{channel_name} exists')
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        








@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(parsed_args.token)
