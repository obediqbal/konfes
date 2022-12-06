from flask import Flask, request
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
  return 'Alive and well'

def run():
    app.run(host='0.0.0.0', port=8080)

def start_server():
    print('starting server')
    t = Thread(target=run)
    t.start()