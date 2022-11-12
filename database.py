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
    avatars_collection = dcdb['avatars']
    user_id = str(avatar.get_user_id())

    cursor = avatars_collection.find({'_id': user_id})[0]
    print(cursor)

db = get_db()
avatars_col = db['avatars']
new_avatar = Avatar(123)
detail = {0: ('obed', 'https://google.com')}
new_avatar.set_detail_in_guild(detail)

print(new_avatar.dumps())

# avatars_col.insert_one()




# myclient = pymongo.MongoClient('mongodb://localhost:27017/')

# mydb = myclient['database']

# mycol = mydb['customers']

# mydict = {'name':'obed','age':19}

# x = mycol.insert_one(mydict)

# print(x.inserted_id)
# print(type(mydb))