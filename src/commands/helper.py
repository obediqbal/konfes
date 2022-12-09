import discord
from discord.ext import commands
import json

class Helper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name='help', description='Learn about my commands')
    async def _help(self, ctx: discord.ApplicationContext):
        with open('src/commands/help.json', 'r') as file:
            embed_json = json.load(file)['embeds']

        embed = discord.Embed.from_dict(embed_json[0])
        
        await ctx.interaction.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Helper(bot))