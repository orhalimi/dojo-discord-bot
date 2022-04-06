# bot.py
import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD1 = os.getenv('DISCORD_GUILD1')
GUILD2 = os.getenv('DISCORD_GUILD2')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

guilds = []
@client.event
async def on_ready():
    guilds.append(discord.utils.get(client.guilds, name = GUILD1))
    guilds.append(discord.utils.get(client.guilds, name = GUILD2))

    
    print(
        f'\n{client.user} is connected to the following guilds:\n'
        f'1) {guilds[0].name} (id: {guilds[0].id})\n2) {guilds[1].name} (id: {guilds[1].id})\n'
    )

    members1 = '\n - '.join([member.name for member in guilds[0].members])
    print(f'Guild1 Members:\n - {members1}')

    members2 = '\n - '.join([member.name for member in guilds[1].members])
    print(f'\nGuild2 Members:\n - {members2}')

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

client.run(TOKEN)