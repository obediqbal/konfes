import pymongo
from avatar import Avatar
import os

class Database:
    def __init__(self) -> None:
        if (os.getenv('PROD') == True):
            print('working')
            self.CONNECTION_STRING = os.getenv('CONNECTION_STRING')
            print(self.CONNECTION_STRING)
        else:
            self.CONNECTION_STRING = os.getenv('CONNECTION_STRING')
        
        self.client = pymongo.MongoClient(self.CONNECTION_STRING)
        self.data = self.client['discord']


    def update_data(self):
        self.data = self.client['discord']


    def update_avatar(self, avatar: Avatar) -> None:
        avatars_col = self.data['avatars']

        avatar_json = avatar.dumps()
        query = {'_id': avatar_json.get('_id')}
        avatars_col.update_one(query, {'$set': avatar_json})

        self.update_data()


    def _insert_avatar_to_db(self, avatar: Avatar) -> None:
        avatars_col = self.data['avatars']

        avatar_json = avatar.dumps()
        avatars_col.insert_one(avatar_json)

        self.update_data()


    def init_avatar(self, user_id: int, guild_id: int) -> Avatar:
        avatar = self.get_avatar(user_id)
        if(avatar == None): # User has never used the bot
            avatar = Avatar(user_id)
            self._insert_avatar_to_db(avatar)

        if(not avatar.is_defined_in_guild(guild_id)): # User has never used the bot in this guild
            avatar.set_detail_in_guild(guild_id, name='Anonymous', asset_url='')
            self.update_avatar(avatar)

        return avatar


    def get_avatar(self, user_id: int) -> Avatar:
        avatars_col = self.data['avatars']

        query = {'_id': str(user_id)}
        json_avatar = avatars_col.find_one(query)

        if(json_avatar == None):
            avatar = None
        else:
            avatar = Avatar.loads(json_avatar)

        return avatar

    
# update_dc_db()

# avatars_col = _global.dc_db['avatars']
# print(avatars_col.find_one({'_id': '555'}))
# new_avatar = Avatar(555)
# # detail = {8: ('rezapu', 'https://yahoo.com')}
# detail = {55: {
#     'name': 'obed',
#     'asset_url': 'https://yahoo.com'
# }}
# new_avatar.set_detail_in_guild(detail)
# detail = {91: {
#     'name': 'rezapu',
#     'asset_url': 'https://google.com'
# }}
# new_avatar.set_detail_in_guild(detail)

# update_avatar_to_db(new_avatar)