import discord
from discord import Webhook
from discord.ext import commands
from avatar import Avatar
import database as db

#https://i.imgur.com/dOzAFCx.png
class Messaging(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @discord.slash_command(name='send', description='Send a message anonymously through your avatar')
    @discord.commands.option(
        "message",
        description = 'Enter your message',
        required = True
    )
    async def _send_message(self, ctx: discord.ApplicationContext, message: str):
        avatar = db.get_avatar_from_db(ctx.user.id)
        if(avatar == None): # User has never used the bot
            avatar = Avatar(ctx.user.id)
            db.insert_avatar_to_db(avatar)
        if(not avatar.is_defined_in_guild(ctx.guild)): # User has never used the bot in this guild
            avatar.set_detail_in_guild('Anonymous', '', ctx.guild)
        db.update_avatar_to_db(avatar)

        (name, avatar_url) = avatar.get_detail_in_guild(ctx.guild)
        newhook = await ctx.channel.create_webhook(name = name)
        await newhook.send(content=message, avatar_url=avatar_url, username=name)

        await newhook.delete()
        await ctx.delete()


    @commands.guild_only()
    @discord.slash_command(name='avatar', description='Setup the configuration of your avatar')
    @discord.commands.option(
        'nickname',
        description = 'This is the name that appears when sending messages',
        required = False,
        default = None
    )
    @discord.commands.option(
        'avatar_url',
        description = 'This is the profile picture of your avatar',
        required = False,
        default = None
    )
    async def _set_avatar(self, ctx: discord.ApplicationContext, nickname:str, avatar_url:str):
        if(nickname == None and avatar_url==None):
            await ctx.delete()
            return

        avatar = db.get_avatar_from_db(ctx.user.id)
        if(avatar == None): # User has never used the bot
            avatar = Avatar(ctx.user.id)
            db.insert_avatar_to_db(avatar)
        if(not avatar.is_defined_in_guild(ctx.guild)): # User has never used the bot in this guild
            avatar.set_detail_in_guild('Anonymous', '', ctx.guild)

        new_name, new_avatar_url = avatar.get_detail_in_guild(ctx.guild)
        if(nickname != None):
            new_name = nickname
        if(avatar_url != None):
            new_avatar_url = avatar_url
        avatar.set_detail_in_guild(new_name, new_avatar_url, ctx.guild)
        
        db.update_avatar_to_db(avatar)

        await ctx.interaction.response.send_message(content='Your avatar has been successfully reconfigured!', ephemeral=True)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


    @_send_message.error
    @_set_avatar.error
    async def private_message_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.errors.NoPrivateMessage):
            await interaction.response.send_message(error)
        else:
            print(error)


def setup(bot: discord.Bot):
    bot.add_cog(Messaging(bot))
