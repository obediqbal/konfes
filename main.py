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
db.update_dc_db()


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.slash_command(name='send', description='Send a message anonymously through your avatar')
async def _send_message(interaction: discord.Interaction, message: str):
    avatar = db.get_avatar_from_db(interaction.user.id)
    if(avatar == None):
        avatar = Avatar(interaction.user.id)
    if(not avatar.is_defined_in_guild(interaction.guild)):
        avatar.set_detail_in_guild('Anonymous', 'https://i.imgur.com/dOzAFCx.png', interaction.guild)
    (name, avatar_url) = avatar.get_detail_in_guild(interaction.guild)

    newhook = await interaction.channel.create_webhook(name = name)
    await newhook.send(content=message, avatar_url=avatar_url, username=name)
    # await newhook.send(content=message, avatar_url='https://i.imgur.com/dOzAFCx.png', username='ini percobaan')
    await newhook.delete()

    await interaction.delete()
    # await interaction.response.send_message('anjayy',ephemeral=True)

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