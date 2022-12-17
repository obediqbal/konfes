import asyncio
import discord
from discord import Webhook
from discord.ext import commands
import os
import database as db
import json
from server import start_server
from dotenv import load_dotenv


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(intents= discord.Intents.all(), command_prefix='!') 
        self.load_extensions(
            'commands.messaging.Messaging',
            'commands.messaging.Config',
            'commands.helper'
            )


    async def on_ready(self):
        db.update_dc_db()
        print('Logged in as:')
        print(self.user.name)

if __name__ == "__main__":
    if (os.getenv('PROD') == True):
        TOKEN = os.getenv('TOKEN')
    else:
        load_dotenv('.env')
        TOKEN = os.getenv('TOKEN')

    bot = Bot()
    
    start_server()
    bot.run(TOKEN) #run the client using using my bot's token

