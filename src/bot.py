from discord.ext import commands
import discord
from database import Database

class KonfesBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(intents= discord.Intents.all(), command_prefix='!') 
        self.load_extensions(
            'commands.messaging.Messaging',
            'commands.messaging.Config',
            'commands.helper'
            )
        self.db = Database()


    async def on_ready(self):
        self.db.update_data()
        print('Logged in as:')
        print(self.user.name)