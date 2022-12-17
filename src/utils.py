import discord
import aiohttp
import io

class Utils:
    @staticmethod
    async def load_image_from_url(url: str, *, parse_to_discord: bool = False):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                img = await resp.read()
                with io.BytesIO(img) as file:
                    if parse_to_discord:
                        file = discord.File(file, 'image.png')
                    return file

    
    @staticmethod
    async def load_images_from_urls(urls: list[str], *, parse_to_discord: bool = False):
        files = []
        for url in urls:
            files.append(await Utils.load_image_from_url(url, parse_to_discord=parse_to_discord))

        return files

    
    def get_refer_embed(refer: discord.Message):
        if refer==None:
            return None

        if len(refer.content) > 300:
            refer.content = refer.content[:200]
            refer.content += f' [...]({refer.jump_url})'

        if refer.webhook_id != None:
            color = 14079702
        else:
            color = refer.author.color.value

        attachment = ''
        if len(refer.attachments)>0:
            attachment = ' <:konfesimage:1052941241811210300>'

        embed_dict = {
                'type': 'rich',
                'color': color,
                'description': f'[\[#\]]({refer.jump_url}) {refer.content}' + attachment,
                'author': {
                    'name': refer.author.display_name,
                    'url': refer.jump_url,
                    'icon_url': refer.author.display_avatar.url
                },
                # "timestamp": message.created_at.isoformat('T')
            }
        embed = discord.Embed.from_dict(embed_dict)
        
        return embed