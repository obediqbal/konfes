# Konfes: Discord Anonymous Messaging

Konfes allows users to send a message anonymously to a server through their own unique configurable avatar. Anonymous voice channel speaking may also be implemented soon.

## Deploying Locally

### Prerequisites
Konfes uses Pycord as a python wrapper for the Discord API, MongoDB to manage its database, and Flask to deploy the web application to the cloud. I will not go into details on either how to deploy a Discord bot or a MongoDB cluster. To install those modules, run

```bash
python -m pip install -r requirements.txt
```

### Setting up environment variables
Required environment variables :
1. `TOKEN`
2. `CONNECTION_STRING`

First thing first, you need to create a `.env` file in the project root's folder, just so
```Properties
TOKEN = your_discord_bot_token
CONNECTION_STRING = your_mongodb_cluster_connection_string
```

### Running the bot

That's it! All you have to do now is to run the bot, simply run `main.py` and you have successfully deployed Konfes locally.

## Contributing

This is just a small project for me and my friends to learn new kinds of stuff. However,
pull requests and feedback are welcome. 

## License

[MIT](https://choosealicense.com/licenses/mit/)