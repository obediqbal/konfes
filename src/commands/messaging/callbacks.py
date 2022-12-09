import discord
import database as db
from avatar import Avatar
from utils import Utils

async def refer_message_callback(message: discord.Message, ctx: discord.ApplicationContext):
    avatar = db.init_avatar_from_db(ctx)
    webhook = await Avatar.get_webhook(ctx)

    (name, avatar_url, *other) = avatar.get_detail_in_guild(ctx.guild)

    embed_dict = {
            "type": "rich",
            "color": 14079702,
            "description": message.content,
            "fields": [
                {
                    "name": '\u200B',
                    "value": f'[Jump!]({message.jump_url})'
                }
            ],
            "author": {
                "name": message.author.name,
                "url": message.jump_url,
                "icon_url": message.author.display_avatar.url
            }
        }
    embed = discord.Embed.from_dict(embed_dict)
    
    await webhook.send(avatar_url=avatar_url, username=name, embed=embed)


async def send_message_callback(ctx: discord.ApplicationContext, message: str, attachments: str):
    await ctx.interaction.response.defer(ephemeral=True)
    avatar = db.init_avatar_from_db(ctx)
    webhook = await Avatar.get_webhook(ctx)

    (name, avatar_url, *other) = avatar.get_detail_in_guild(ctx.guild)

    attachments = attachments.split()
    files = await Utils.load_images_from_urls(attachments, parse_to_discord=True)

    if (message==None and files==[]):
        await ctx.interaction.followup.send(content='Can\'t send an empty message!', ephemeral=True, delete_after=5.0)
    else:
        await webhook.send(content=message, avatar_url=avatar_url, username=name, files=files)
        await ctx.interaction.followup.send(content='Message sent!', ephemeral=True, delete_after=1.0)