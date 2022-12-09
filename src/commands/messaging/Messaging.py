import discord
from discord import Webhook
from discord.ext import commands
from avatar import Avatar
from utils import Utils
from modals import Modal
import commands.messaging.callbacks as callbacks
import database as db
import traceback

#https://i.imgur.com/dOzAFCx.png
class Messaging(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @discord.slash_command(name='send', description='Send a message anonymously through your avatar')
    @discord.commands.option(
        'message',
        description = 'Enter your message',
        required = False,
        default = None
    )
    @discord.commands.option(
        'attachments',
        description = 'Attach images, seperate each urls with a space',
        required = False,
        default = ''
    )
    async def _send_message(self, ctx: discord.ApplicationContext, message: str, attachments: str):
        await callbacks.send_message_callback(ctx=ctx, message=message, attachments=attachments)


    @commands.guild_only()
    @discord.slash_command(name='reply', description='Reply to a message')
    @discord.commands.option(
        'message_id',
        description = 'ID of the message you are replying to',
        required = True
    )
    @discord.commands.option(
        'message',
        description = 'Enter your message',
        required = False,
        default = None
    )
    @discord.commands.option(
        'attachments',
        description = 'Attach images, seperate each urls with a space',
        required = False,
        default = ''
    )
    async def _reply_message(self, ctx: discord.ApplicationContext, message_id: str, message: str, attachments: str):
        message_id = int(message_id)
        refer = await ctx.channel.fetch_message(message_id)

        await callbacks.refer_message_callback(refer, ctx)
        await callbacks.send_message_callback(ctx, message=message, attachments=attachments)


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

        avatar = db.init_avatar_from_db(ctx)

        new_name, new_avatar_url, *other = avatar.get_detail_in_guild(ctx.guild)
        if(nickname != None):
            new_name = nickname
        if(avatar_url != None):
            new_avatar_url = avatar_url
        avatar.set_detail_in_guild(ctx.guild, name=new_name, asset_url=new_avatar_url)
        
        db.update_avatar_to_db(avatar)

        await ctx.interaction.response.send_message(content='Your avatar has been successfully reconfigured!', ephemeral=True)


    # @discord.commands.message_command(name='Reply')
    # async def _reply(self, message: discord.Message, ctx: discord.ApplicationContext):
    #     print(message.message)
    #     print(message.interaction.id)
    #     print(message.interaction.message)
    #     print(await message.interaction.original_response())
    #     modal = Modal.reply_modal(ctx=message)
    #     await message.interaction.response.send_modal(modal)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


    @_send_message.error
    @_set_avatar.error
    async def private_message_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.errors.NoPrivateMessage):
            await interaction.response.send_message(error)
        else:
            traceback.print_exc()


def setup(bot: discord.Bot):
    bot.add_cog(Messaging(bot))
