import asyncio
import discord
from discord import Webhook
from discord.ext import commands
import database as db
from avatar import Avatar
import json

with open('auth.json') as file:
    data = json.load(file)
    TOKEN = data['token']

bot = commands.Bot(intents= discord.Intents.all(), command_prefix='/') #define command decorator

@bot.event
async def on_message(message):
    await bot.process_commands(message)

# @bot.command(pass_context=True) #define the first command and set prefix to '!'
# async def rename(ctx, name):

@bot.slash_command(name='send', description='Send a message anonymously through your avatar')
async def _send_message(interaction: discord.Interaction, message: str):
    # avatar = discord.Asset(state='',url='https://i.imgur.com/dOzAFCx.png')
    newhook = await interaction.channel.create_webhook()
    await newhook.send(content=message, avatar_url='https://i.imgur.com/dOzAFCx.png', username='ini percobaan')
    await newhook.delete()
    await interaction.response.send_message('anjayy',ephemeral=True)

@bot.command()
async def ping(ctx):
    await ctx.guild.me.edit(nick='Pinger')
    await ctx.send('Pong!')
    await asyncio.sleep(1)
    await ctx.guild.me.edit(nick=None)

# @bot.command()
# async def create_hook(ctx, arg):
#     newhook = await ctx.channel.create_webhook(name='ini percobaan')
#     await newhook.send(content='haloo ges')
#     await newhook.delete()

@bot.event #print that the bot is ready to make sure that it actually logged on
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    # await bot.change_presence(game=Game(name="in rain ¬ !jhelp"))

bot.run(TOKEN) #run the client using using my bot's token