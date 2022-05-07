import sys
import os
import random
import discord
from discord.ext import commands
from . import utils


def get_configs():
    guilds_config = utils.read_yaml_file("configs/guilds.yaml").get("guilds", [])
    commands_config = utils.read_yaml_file("configs/commands.yaml").get("commands", [])

    return {"guilds_config": guilds_config, "commands_config": commands_config}


def get_bot_settings():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Something went wrong with the discord token")
        sys.exit()

    configs = get_configs()

    return {
        "token": token,
        "command_prefix": "!",
        "intents": discord.Intents.all(),
        **configs,
    }


def main():
    settings = get_bot_settings()
    token = settings.get("token")
    intents = settings.get("intents", discord.Intents.all())
    command_prefix = settings.get("command_prefix", "!")

    bot = commands.Bot(command_prefix=command_prefix, intents=intents)

    # EVENTS
    @bot.event
    async def on_ready():
        print(f"{bot.user.name} has connected to Discord!")

    @bot.event
    async def on_member_join(member):
        """
        Send a greeting to members upon joining the server
        """
        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have the correct role for this command.")

    # COMMANDS
    @bot.command(
        name="private_channel",
        help="Creates private channel with the member names that is provided",
    )
    # @commands.has_role('admin')
    async def create_private_channel(
        ctx,
        room_name,
        *members: discord.Member,
    ):
        """
        Takes 2 parameters: A room name and a list of tagged members to be added to the room.
        Creates a private room with the room name and addes the members to that room.
        Room name must not already exist in the server.
        """

        if room_name is None:
            await ctx.send(
                """
                Room name is empty,
                please add a room name to the command (after the last member to the be added to the room)"
                """
            )
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
                overwrites[member] = discord.PermissionOverwrite(read_messages=True)

            existing_channels = discord.utils.get(guild.channels, name=room_name)
            if not existing_channels:
                members_names = (",").join(member_list)
                await guild.create_text_channel(room_name, overwrites=overwrites)
                await ctx.send(
                    f"Creating a private channel called {room_name} and adding {members_names} to it."
                )
            else:
                await ctx.send(
                    f"A room with the name: {room_name} already exists. Please choose a different name."
                )

    # Reply to a !99 message with a random Peralta quote
    @bot.command(name="99", help="Responds with a random quote from Brooklyn 99")
    async def nine_nine(ctx):
        brooklyn_99_quotes = [
            "I'm the human form of the 💯 emoji.",
            "Bingpot!",
            (
                "Cool. Cool cool cool cool cool cool cool, "
                "no doubt no doubt no doubt no doubt."
            ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @bot.command(name="roll_dice", help="Simulates rolling dice.")
    async def roll(ctx, number_of_dice: int, number_of_sides: int):
        """
        A !roll_dice message should be accompanied with 2 numbers -
        1. number of dices
        2. number of sides each dice has
        Roll the dice and return the sum of random numvers received
        """
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(", ".join(dice))

    bot.run(token)


if __name__ == "__main__":
    main()
