''' details reminder is a function that activates once a week to remind members of the dojo to register their information so the admin can easily contact them if'''

import argparse
import logging
import json
import discord
from discord.ext import commands
from core import Core


ON_READY_MSG = "Name phone function is activating!"


class phoneReminder(commands.Bot):
    ''' this function recive an room id and just sent an message about upcoming event '''

    def __init__(self):
        intents = discord.Intents.all()
        self.core = Core()
        commands.Bot.__init__(self, intents=intents, command_prefix="!!!")

    def start_bot(self):
        ''' to be able to run the bot from other file '''

        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--token", dest="token", help="token")
        args = parser.parse_args()
        bot = phoneReminder()
        bot.run(args.token)

    async def remind_name_phone(self) -> None:
        '''this function checks which of the current users in our DB did not register private details and sends them a PM reminding them to do so'''
        guild = self.guilds[0]
        data = self.core.get('profiles/')
        profiles = json.loads(data.text)
        members = guild.members
        for m in profiles:
            if m['subscribed']:
                if m['real_name'] == None or m['phone_number'] == None:
                    user_id = m['id']
                    member = discord.utils.find(lambda m: m.id == user_id, members)
                    await member.send('This is a reminder to please update your details in the Dojo DB, to do so use the command: !namephone followed by your first name and phone number (here or in your private mentoring room) Example: !namephone FirstName 0505555555, If you do not wish to see this message again you can reply with "!namephone unsubscribe" and you will not be contacted about this again')

    async def on_ready(self) -> None:
        ''' this function recive an room id and just sent an message about upcoming event '''
        print(ON_READY_MSG)
        logging.debug(ON_READY_MSG)
        await self.remind_name_phone()
