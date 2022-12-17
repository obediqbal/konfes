import discord
import database as db
from avatar import Avatar
from utils import Utils
# import datetime

async def send_message_callback(ctx: discord.ApplicationContext, message: str, attachments: str, refer: discord.Message = None):
    avatar = db.init_avatar_from_db(ctx)
    webhook = await Avatar.get_webhook(ctx)
    embed = Utils.get_refer_embed(refer)

    (name, avatar_url, *other) = avatar.get_detail_in_guild(ctx.guild)

    attachments = attachments.split()
    files = await Utils.load_images_from_urls(attachments, parse_to_discord=True)

    if (message==None and files==[]):
        await ctx.interaction.followup.send(content='Can\'t send an empty message!', ephemeral=True, delete_after=5.0)
    else:
        await webhook.send(content=message, avatar_url=avatar_url, username=name, files=files, embed=embed)