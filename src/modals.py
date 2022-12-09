import database as db
from avatar import Avatar
from utils import Utils
import discord

class Modal(discord.ui.Modal):
    def __init__(self, *children, callback, title) -> None:
        super().__init__(*children, title=title)
        self.callback = callback


    async def on_submit(self):
        await self.callback()


    @staticmethod
    def reply_modal(ctx: discord.ApplicationContext):
        message_input = discord.ui.InputText(label='Message', style=discord.InputTextStyle.long)
        attachments_input = discord.ui.InputText(label='Attachments', style=discord.InputTextStyle.long)

    


        embed_dict = {
                "type": "rich",
                "color": 14079702,
                "description": ctx.interaction.message.content,
                "author": {
                    "name": ctx.author.name,
                    "url": ctx.interaction.jump_url,
                    "icon_url": ctx.author.display_avatar.url
                },
                "footer": {
                    "text": f'[Jump!]({ctx.interaction.message.jump_url})'
                }
            }
        embed = discord.Embed.from_dict(embed_dict)

        async def callback(interaction: discord.Interaction):
            content = message_input.value
            attachments = attachments_input.value

            avatar = db.init_avatar_from_db(ctx)
            webhook = await Avatar.get_webhook(ctx)

            (name, avatar_url, *other) = avatar.get_detail_in_guild(ctx.guild)

            attachments = attachments.split()
            files = await Utils.load_images_from_urls(attachments, parse_to_discord=True)

            if (content==None and files==[]):
                await interaction.response.send_message(content='Can\'t send an empty message!', ephemeral=True, delete_after=5.0)
            else:
                await webhook.send(embed=embed)
                await webhook.send(content=content, avatar_url=avatar_url, username=name, files=files)
                await interaction.response.send_message(content='Message sent!', ephemeral=True, delete_after=1.0)

        modal = Modal(message_input, attachments_input, title='Reply', callback=callback)

        return modal
