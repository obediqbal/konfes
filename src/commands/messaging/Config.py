import discord
from discord.ext import commands
from bot import KonfesBot
import exceptions
import traceback

class Config(commands.Cog):
    def __init__(self, bot: KonfesBot):
        self.bot = bot


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
        await ctx.interaction.response.defer(ephemeral=True)
        if(nickname == None and avatar_url==None):
            raise exceptions.AllOptionsUnselectedException()

        avatar = self.bot.db.init_avatar(ctx.author.id, ctx.guild_id)

        new_name, new_avatar_url, *other = avatar.get_detail_in_guild(ctx.guild_id)
        if(nickname != None):
            new_name = nickname
        if(avatar_url != None):
            new_avatar_url = avatar_url
        avatar.set_detail_in_guild(ctx.guild_id, name=new_name, asset_url=new_avatar_url)
        
        self.bot.db.update_avatar(avatar)

        await ctx.interaction.followup.send(content='Your avatar has been successfully reconfigured!', ephemeral=True)


    @commands.guild_only()
    @discord.slash_command(name='morph', description='Morph into someone\'s avatar')
    @discord.commands.option(
        'message_id',
        description = 'The message of someone you want to morph into',
        required = True
    )
    async def _morph(self, ctx: discord.ApplicationContext, message_id: str):
        await ctx.interaction.response.defer(ephemeral=True)

        avatar = self.bot.db.init_avatar(ctx.author.id, ctx.guild_id)
        
        message_id = int(message_id)
        refer = await ctx.channel.fetch_message(message_id)
        if refer==None:
            raise discord.errors.NotFound

        avatar.set_detail_in_guild(ctx.guild_id, name=refer.author.display_name, asset_url=refer.author.display_avatar.url)
        self.bot.db.update_avatar(avatar)

        await ctx.interaction.followup.send(content=f'Successfully morphed into {refer.author.display_name}', ephemeral=True)


    @_set_avatar.error
    @_morph.error
    async def handler(self, interaction: discord. Interaction, error):
        if isinstance(error.original, exceptions.AllOptionsUnselectedException):
            await interaction.followup.send(error.original, ephemeral=True)
        if isinstance(error.original, discord.errors.NotFound):
            await interaction.followup.send('Message not found', ephemeral=True)
        else:
            traceback.print_exc()


def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))