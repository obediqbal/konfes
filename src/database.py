import pymongo
import discord
from avatar import Avatar
import json
import os
import _global as _global

if (os.getenv('PROD') == True):
    print('working')
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    print(CONNECTION_STRING)
else:
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')


def update_dc_db():
    _global.dc_db = get_db('discord')


def get_db(name:str) -> pymongo.database.Database:
    client = pymongo.MongoClient(CONNECTION_STRING)

    return client[name]


def update_avatar_to_db(avatar: Avatar) -> None:
    avatars_col = _global.dc_db['avatars']

    avatar_json = avatar.dumps()
    query = {'_id': avatar_json.get('_id')}
    avatars_col.update_one(query, {'$set': avatar_json})

    update_dc_db()


def insert_avatar_to_db(avatar: Avatar) -> None:
    avatars_col = _global.dc_db['avatars']

    avatar_json = avatar.dumps()
    avatars_col.insert_one(avatar_json)

    update_dc_db()


def init_avatar_from_db(ctx: discord.ApplicationContext) -> Avatar:
    avatar = get_avatar_from_db(ctx.user.id)
    if(avatar == None): # User has never used the bot
        avatar = Avatar(ctx.user.id)
        insert_avatar_to_db(avatar)

    if(not avatar.is_defined_in_guild(ctx.guild)): # User has never used the bot in this guild
        avatar.set_detail_in_guild(ctx.guild, name='Anonymous', asset_url='')
        update_avatar_to_db(avatar)

    return avatar


def get_avatar_from_db(user_id: int) -> Avatar:
    avatars_col = _global.dc_db['avatars']

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