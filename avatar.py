import discord
import json
from typing import overload

class Avatar:
    def __init__(self, user_id: int) -> None:
        self._user_id = user_id
        self.details:dict[discord.Guild.id, tuple[str, str]] = dict() # {guild_id : (name, asset_url)}

    
    def get_user_id(self) -> int:
        return self._user_id


    def get_user(self, bot: discord.Bot) -> discord.User:
        return bot.get_user(self._id)


    def get_member(self, guild: discord.Guild) -> discord.Member:
        return guild.get_member(self._user_id)


    def get_details_on_guild(self, guild: discord.Guild) -> tuple[str, str]:
        guild_id = guild.id
        return (self.details.get(guild_id).name, self.details.get(guild_id).asset_url)


    def is_defined_in_guild(self, guild: discord.Guild) -> bool:
        return guild.id in self.details.keys()


    @overload
    def set_detail_in_guild(self, name: str, asset_url: str, guild: discord.Guild) -> None:
        detail = {guild.id: (name, asset_url)}
        self.details.update(detail)


    def set_detail_in_guild(self, detail:tuple[str, str]) -> None:
        self.details.update(detail)


    def dumps(self) -> dict:
        json_details = json.loads(json.dumps(self.details))

        return {'_id': str(self._user_id), 'details': json_details}

    # def loads(self, ) -> None:
