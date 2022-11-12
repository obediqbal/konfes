import pymongo
from avatar import Avatar
import json
import _global

with open('auth.json') as file:
    data = json.load(file)
    CONNECTION_STRING = data['connection_string']


def update_dc_db():
    _global.dc_db = get_db('discord')


def get_db(name:str) -> pymongo.database.Database:
    client = pymongo.MongoClient(CONNECTION_STRING)

    return client[name]


def update_avatar_to_db(avatar: Avatar) -> None:
    avatars_col = _global.dc_db['avatars']

    avatar_json = avatar.dumps()
    query = {"_id": avatar_json.get('_id')}
    avatars_col.update_one(query, {'$set': avatar_json})

    update_dc_db()
    

# update_dc_db()

# avatars_col = _global.dc_db['avatars']
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