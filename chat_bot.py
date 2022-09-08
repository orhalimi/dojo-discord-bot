''' chat bot  '''

from dataclasses import dataclass
from urllib.parse import uses_relative
import discord
import argparse
from discord.ext import commands
from discord.utils import get, find
from core import Core
import logging
import datetime
import json

ON_READY_MSG = "ChatBot is waking up!"
LOG_PWD = "logs/bots/chat_bot.log"
LOG_FMT = "%(asctime)s | %(message)s"
ADDRESS = "http://127.0.0.1:8000/api/"


class DiscordBot(commands.Bot):
    def __init__(self):
        logging.basicConfig(filename=LOG_PWD, level=logging.DEBUG, format=LOG_FMT)
        self.core = Core()
        intents = discord.Intents.all()
        commands.Bot.__init__(self, command_prefix="!",
                              intents=intents, case_insensitive=True)
        self.add_commands()

    async def on_ready(self) -> None:
        print(ON_READY_MSG)
        logging.debug(ON_READY_MSG)

    async def on_member_join(self, member) -> None:
        await member.create_dm()
        logging.debug("on_member_join -> function call")
        await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")

    async def on_command_error(self, ctx, error) -> None:
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have the correct role for this command.")

    async def on_message(self, ctx) -> None:

        if not ctx.content.startswith("!"):
            content = ctx.content

            if ctx.author != self.user:
                if self.core.exist("profiles", ctx.author.id) == False:
                    profile_data = {
                        "id": ctx.author.id,
                        "discord_name": ctx.author.display_name,
                    }

                    self.core.post("profiles", profile_data)
                    #

                if self.core.exist("rooms", ctx.channel.id) == False:
                    room_data = {"id": ctx.channel.id}

                    self.core.post("rooms", room_data)
                    #

                message_data = {
                    "content": content,
                    "profile": ADDRESS
                    + "profiles/"
                    + str(ctx.author.id)
                    + "/",
                    "room": ADDRESS + "rooms/" + str(ctx.channel.id) + "/",
                }

                self.core.post("messages", message_data)

        await self.process_commands(ctx)

    def add_commands(self) -> None:
        @self.command(name="event")
        async def make_event(ctx, date: str, time: str) -> None:
            # TODO: add regex? more support!
            date = date.split("/")
            time = time.split(":")

            date_and_time = datetime.datetime(
                int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])
            )

            event_data = {
                "room": ADDRESS + "rooms/" + str(ctx.channel.id) + "/",
                "target_date_and_time": date_and_time,
            }
            if self.core.post("events", event_data):
                logging.debug("event created!")
                await ctx.send(
                    f"Creating Event on channel! you will remined by me 15 minutes before {time[0]}:{time[1]} at the {date[0]}/{date[1]}/{date[2]}"
                )
            else:
                await ctx.send(f"Event info is wrong")

        @self.command(name="summary")
        async def make_summary(ctx, *, content: str) -> None:
            summary_data = {
                "content": content,
                "profile": ADDRESS + "profiles/" + str(ctx.author.id) + "/",
                "room": ADDRESS + "rooms/" + str(ctx.channel.id) + "/",
            }

            if self.core.post("summaries", summary_data):
                logging.debug("summary created!")
                await ctx.send(f"Summary submitted successfully")
            else:
                await ctx.send(f"Something in summary information is wrong")

        @self.command(name="private")
        async def make_private_channel(ctx, *members: discord.Member) -> None:
            guild = ctx.guild

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
            }

            for member in members:
                overwrites[member] = discord.PermissionOverwrite(read_messages=True)

            room_name = f"{members[1].display_name} mentors {members[0].display_name}"

            existing_channels = discord.utils.get(guild.channels, name=room_name)

            if not existing_channels:
                members_str = ", ".join(m.name for m in members)
                channel = await guild.create_text_channel(
                    room_name, overwrites=overwrites
                )
                await channel.send(f"Please read this document to learn how the mentoring program works: https://docs.google.com/document/d/1Zl0ul8B_TrcOgWw2iielkcgeYXNLcepxfeMQEyco8o8/edit")
                room_path = ADDRESS + "rooms/" + str(channel.id) + "/"

            room_data = {"id": channel.id}
            self.core.post("rooms", room_data)

            for index in range(len(members)):

                profile_data = {
                    "id": members[index].id,
                    "discord_name": members[index].name,
                    "real_name": None,
                    "phone_number": None,
                    "subscribed": True,
                }

                member_data = {
                    "profile": ADDRESS
                    + "profiles/"
                    + str(members[index].id)
                    + "/",
                    "role": ADDRESS + "roles/" + str(index + 1) + "/",
                    "room": room_path,
                }

                if self.core.exist("profiles", members[index].id):
                    self.core.post("members", member_data)
                else:
                    self.core.post("profiles", profile_data)
                    self.core.post("members", member_data)

            logging.debug("private channel created!")
            await ctx.send(
                f"Creating a private channel called {room_name} and adding {members_str} to it."
            )
            return

        @self.command(name="namephone")
        async def update_name_phone(ctx, *details: str) -> None:
            print(details)
            member = ctx.author
            if details[0] == 'unsubscribe':
                print('works')
                new_details = {
                    "id": member.id,
                    "discord_name": member.name,
                    "real_name": None,
                    "phone_number": None,
                    "subscribed": "false",
                }
                self.core.update("profiles", new_details, member.id)
                print('works2')
                await ctx.channel.send(f'Unsubscribed, You won\'t get this message again.')
            elif len(details) != 2:
                await ctx.channel.send('Incorrect data sent, please send 2 things after the !namephone command: first name and phone number. Example: !namephone myName 0505555555 ')
            else:
                new_details = {
                    "id": member.id,
                    "discord_name": member.name,
                    "real_name": details[0],
                    "phone_number": details[1],
                    "subscribed": "true",
                }
                if self.core.exist("profiles", member.id):
                    self.core.update("profiles", new_details, member.id)
                    await ctx.channel.send(f'Thank you for updating your details {member.name}!')
                else:
                    await ctx.channel.send(f'{member.name} - There is no profiles registered with your details (discord ID etc) please contact the program admin to fix this.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", dest="token", help="tkn")
    args = parser.parse_args()
    bot = DiscordBot()
    bot.run(args.token)
