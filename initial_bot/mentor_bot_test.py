# bot.py
import os
import discord
import random
import argparse

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', dest = 'token', help = "If you don't have the token please ask Eran to send it to you")
    parser.add_argument('-g', '--guild_name', dest = 'guild', default = "Dojo bots lab")
    return parser.parse_args()

parsed_args = parse_arguments()
#
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name = parsed_args.guild)
    print(f'\n{client.user} is connected to {guild.name} (id: {guild.id})')

    guild_members =  '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {guild_members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(parsed_args.token)