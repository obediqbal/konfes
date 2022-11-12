import pymongo
from avatar import Avatar
import json

with open('auth.json') as file:
    data = json.load(file)
    CONNECTION_STRING = data['connection_string']


def get_db(name:str ='discord') -> pymongo.database.Database:
    client = pymongo.MongoClient(CONNECTION_STRING)

    return client[name]


def update_avatar_to_db(avatar: Avatar) -> None:
    dcdb = get_db()
    avatars_col = dcdb['avatars']

    avatar_json = avatar.dumps()
    query = {"_id": avatar_json.get('_id')}
    avatars_col.update_one(query, {'$set': avatar_json})
    

# db = get_db()
# avatars_col = db['avatars']
# new_avatar = Avatar(555)
# # detail = {8: ('rezapu', 'https://yahoo.com')}
# detail = {31: {
#     'name': 'obed',
#     'asset_url': 'https://yahoo.com'
# }}
# new_avatar.set_detail_in_guild(detail)
# detail = {8: {
#     'name': 'rezapu',
#     'asset_url': 'https://google.com'
# }}
