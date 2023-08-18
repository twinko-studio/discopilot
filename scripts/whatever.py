
from discopilot.configuration_loader import ConfigurationLoader

from interactions import Client, Intents, listen
from interactions import slash_command, SlashContext

import discord
# from discord.ext import commands
from discord import app_commands

config = ConfigurationLoader.load_config()
gid = config['Discord']['TS_GUILD_ID']

## discord.py
intents = discord.Intents.default()  
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name = "commandname", description = "My first application Command", guild=discord.Object(id=gid)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=gid))
    print("Ready!")

client.run(config['Discord']['DISCORD_BOT_TOKEN'])


## interaction.py

bot = Client(intents=Intents.DEFAULT)

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    # This event is called when a message is sent in a channel the bot can see
    print(f"message received: {event.message.content}")


@slash_command(name="my_command", description="My first command :)")
async def my_command_function(ctx: SlashContext):
    await ctx.send("Hello World")

@slash_command(name="my_long_command", description="My second command :)")
async def my_long_command_function(ctx: SlashContext):
    # need to defer it, otherwise, it fails
    await ctx.defer()

    # do stuff for a bit
    await asyncio.sleep(600)

    await ctx.send("Hello World")


bot.start(config['Discord']['DISCORD_BOT_TOKEN'])

