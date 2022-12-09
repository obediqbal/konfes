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