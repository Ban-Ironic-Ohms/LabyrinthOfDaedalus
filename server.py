from flask import Flask
from main import main

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'