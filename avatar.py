import discord
import json
from typing import overload

class Avatar:
    def __init__(self, user_id: int) -> None:
        self._user_id = user_id
        self.details:dict[discord.Guild.id, dict[str, str]] = dict() # {guild_id : {name, asset_url}}

    
    def get_user_id(self) -> int:
        return self._user_id


    def get_user(self, bot: discord.Bot) -> discord.User:
        return bot.get_user(self._user_id)


    def get_member(self, guild: discord.Guild) -> discord.Member:
        return guild.get_member(self._user_id)


    def get_details_in_guild(self, guild: discord.Guild) -> tuple[str, str]:
        guild_id = guild.id
        return (self.details.get(guild_id).get('name'), self.details.get(guild_id).get('asset_url'))


    def is_defined_in_guild(self, guild: discord.Guild) -> bool:
        return guild.id in self.details.keys()


    @overload
    def set_detail_in_guild(self, name: str, asset_url: str, guild: discord.Guild) -> None:
        detail = {guild.id: {'name':name, 'asset_url':asset_url}}
        self.details.update(detail)


    def set_detail_in_guild(self, detail:tuple[str, str]) -> None:
        self.details.update(detail)


    def dumps(self) -> dict:
        json_avatar = json.loads(json.dumps(self.__dict__))
        json_avatar.update({'_id': str(self._user_id)})
        json_avatar.pop('_user_id')

        return json_avatar


    @staticmethod
    def loads(json_avatar: dict):
        new = Avatar(0)
        new._user_id = int(json_avatar.get('_id'))

        new.details = {int(key):json_avatar.get('details').get(key) for key in json_avatar.get('details')}

        return new

