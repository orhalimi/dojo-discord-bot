''' reminder bot had a small amount of responsibilities and behaviors, mainly, he just sent reminder about upcoming events '''

import re
import sys
import logging
from functools import lru_cache
import argparse
import datetime as dt
import json
import discord
from discord.ext import commands
from core import Core

LOG_PWD = "logs/bots/reminder_bot.log"
LOG_FMT = "%(asctime)s | %(message)s"
MINUTES_BEFORE_MSG = 15
MSG_TEMPLATE = "Reminder!"
ON_READY_MSG = "ReminderBot is wake's up!"

class ReminderBot(commands.Bot):
    ''' this function recive an room id and just sent an message about upcoming event '''

    def __init__(self):
        logging.basicConfig(filename=LOG_PWD, level=logging.DEBUG, format=LOG_FMT)
        intents = discord.Intents.all()
        self.core = Core()
        commands.Bot.__init__(self, intents=intents, command_prefix="!!!")

    def start_bot(self):
        ''' to be able to run the bot from other file '''

        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--token", dest="token", help="token")
        args = parser.parse_args()
        bot = ReminderBot()
        bot.run(args.token)

    @lru_cache(maxsize=64)
    async def search_events(self):
        ''' this function search for events in the current day and call to sent_reminder if founded '''

        response = self.core.get("events")
        json_data = json.loads(response.text)

        for index, event in enumerate(json_data):
            event_date = dt.datetime.fromisoformat(event["target_date_and_time"])
            event_is_today: bool = event_date.date() == dt.datetime.today().date()

            if event_is_today:
                event_minute = event_date.minute - MINUTES_BEFORE_MSG
                today_time = dt.datetime.now().time()
                event_room_id = re.findall("[0-9]{19}", event["room"])[-1]

                print(f"{index}, room:{event_room_id} be notify at {event_date.hour}:{event_minute}")
                if today_time.hour == event_date.hour and today_time.minute == event_minute:
                    await self.sent_reminder(int(event_room_id))
        return sys.exit(0)

    async def sent_reminder(self, room_id: int):
        ''' this function recive an room id and just sent an message about upcoming event '''

        channel = self.get_channel(room_id)
        if channel is not None:
            await channel.send(MSG_TEMPLATE)
        else:
            logging.critical("could not find this channel! maybe the input type is diffrent?")

    async def on_ready(self) -> None:
        ''' this function recive an room id and just sent an message about upcoming event '''
        
        print(ON_READY_MSG)
        logging.debug(ON_READY_MSG)
        await self.search_events()
