import asyncio
import discord
from discord import Webhook
from discord.ext import commands
import os
import database as db
import json
from server import start_server


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(intents= discord.Intents.all(), command_prefix='!') 
        self.load_extension('commands.Messaging')


    async def on_ready(self):
        db.update_dc_db()
        print('Logged in as:')
        print(self.user.name)

if __name__ == "__main__":
    if (os.environ.get('IS_HEROKU', None)):
        TOKEN = os.getenv('token')
    else:
        with open('./src/auth.json') as file:
            data = json.load(file)
            TOKEN = data['token']
    
    bot = Bot()
    
    start_server()
    bot.run(TOKEN) #run the client using using my bot's token
