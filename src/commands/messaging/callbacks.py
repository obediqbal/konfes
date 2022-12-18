import discord
from database import Database
from avatar import Avatar
from utils import Utils
# import datetime

async def send_message_callback(ctx: discord.ApplicationContext, message: str, attachments: str, db: Database, refer: discord.Message = None):
    avatar = db.init_avatar(ctx.author.id, ctx.guild_id)
    webhook = await Avatar.get_webhook(ctx.channel)
    embed = Utils.get_refer_embed(refer)

    (name, avatar_url, *other) = avatar.get_detail_in_guild(ctx.guild_id)

    attachments = attachments.split()
    files = await Utils.load_images_from_urls(attachments, parse_to_discord=True)

    if (message==None and files==[]):
        await ctx.interaction.followup.send(content='Can\'t send an empty message!', ephemeral=True, delete_after=5.0)
    else:
        await webhook.send(content=message, avatar_url=avatar_url, username=name, files=files, embed=embed)