import discord
from discord.ext import commands
import database as db
import exceptions

class Config(commands.Cog):
    def __init__(self, bot: commands.bot):
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

        avatar = db.init_avatar_from_db(ctx)

        new_name, new_avatar_url, *other = avatar.get_detail_in_guild(ctx.guild)
        if(nickname != None):
            new_name = nickname
        if(avatar_url != None):
            new_avatar_url = avatar_url
        avatar.set_detail_in_guild(ctx.guild, name=new_name, asset_url=new_avatar_url)
        
        db.update_avatar_to_db(avatar)

        await ctx.interaction.followup.send(content='Your avatar has been successfully reconfigured!', ephemeral=True)


    @_set_avatar.error
    async def handler(self, interaction: discord. Interaction, error):
        if isinstance(error.original, exceptions.AllOptionsUnselectedException):
            await interaction.followup.send(error.original, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))