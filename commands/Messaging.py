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
    async def _send_message(self, interaction: discord.Interaction, message: str):
        avatar = db.get_avatar_from_db(interaction.user.id)
        if(avatar == None): # User has never used the bot
            avatar = Avatar(interaction.user.id)
            db.insert_avatar_to_db(avatar)
        if(not avatar.is_defined_in_guild(interaction.guild)): # User has never used the bot in this guild
            avatar.set_detail_in_guild('Anonymous', '', interaction.guild)
        db.update_avatar_to_db(avatar)

        (name, avatar_url) = avatar.get_detail_in_guild(interaction.guild)
        newhook = await interaction.channel.create_webhook(name = name)
        await newhook.send(content=message, avatar_url=avatar_url, username=name)

        await newhook.delete()
        await interaction.delete()


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


    @_send_message.error
    async def _send_message_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.errors.NoPrivateMessage):
            await interaction.response.send_message(error)


def setup(bot: discord.Bot):
    bot.add_cog(Messaging(bot))
