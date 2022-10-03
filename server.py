import re
from warnings import catch_warnings
from flask import Flask
from main import main
import firebase_admin

def listener(event):
    print(event.event_type)
    print(event.path)
    print(event.data)
    

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
    
@app.route('/')
def out(message=""):
    try:
        print(message.data)
        return message.data
    except:
        return "error"

firebase_admin.db.reference('/message/').listen(out)

@app.route('/')
def hello_world():
    print("hello")
    return 'Hello, World!'

hello_world()