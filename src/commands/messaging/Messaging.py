import discord
from discord.ext import commands
from bot import KonfesBot
# from modals import Modal
import commands.messaging.callbacks as callbacks
# import database as db

import traceback

#https://i.imgur.com/dOzAFCx.png
class Messaging(commands.Cog):
    def __init__(self, bot: KonfesBot):
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
        await ctx.interaction.response.defer(ephemeral=True)

        await callbacks.send_message_callback(ctx=ctx, message=message, attachments=attachments, db=self.bot.db)

        await ctx.interaction.followup.send(content='Success', ephemeral=True, delete_after=1.0)


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
        await ctx.interaction.response.defer(ephemeral=True)

        message_id = int(message_id)
        refer = await ctx.channel.fetch_message(message_id)
        if(refer == None):
            raise discord.errors.NotFound
        elif((refer.content == '' and refer.attachments == []) or (message==None and attachments=='')):
            raise discord.errors.InvalidArgument
        else:
            await callbacks.send_message_callback(ctx, message=message, attachments=attachments, refer=refer, db=self.bot.db)

        await ctx.interaction.followup.send(content='Success', ephemeral=True, delete_after=1.0)


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
    @_reply_message.error
    # @_set_avatar.error
    async def message_error(self, interaction:discord.Interaction, error):
        print(type(error))
        if isinstance(error, commands.errors.NoPrivateMessage):
            await interaction.response.send_message(error)
        if isinstance(error.original, discord.errors.NotFound):
            await interaction.followup.send('Message not found', ephemeral=True, delete_after=5.0)
        else:
            await interaction.followup.send('Failed', ephemeral=True, delete_after=5.0)
            traceback.print_exc()


def setup(bot: discord.Bot):
    bot.add_cog(Messaging(bot))
