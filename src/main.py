import os
from server import start_server
from dotenv import load_dotenv
from bot import KonfesBot

if __name__ == "__main__":
    if (os.getenv('PROD') == True):
        TOKEN = os.getenv('TOKEN')
    else:
        load_dotenv('.env')
        TOKEN = os.getenv('TOKEN')

    bot = KonfesBot()
    
    start_server()
    bot.run(TOKEN) #run the client using using my bot's token

