# Thanks to github.com/mdrkb for this template. I could not find documentation for this
from xml.dom import ValidationErr
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebase-keys.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com/'
})
    
class Firebase:
    def __init__(self, reset=False, base=True):
        if reset:
            with open("Firebase/init.json") as file:
                data = json.load(file)

            ref = db.reference('/')
            ref.set(data)
            
            if base:
                with open("Rooms/room_example.json") as file:
                    rm_ex = json.load(file)
                with open("Rooms/room_example_connector.json") as file:
                    rm_ex_con = json.load(file)
                with open("Rooms/player_data.json") as file:
                    player = json.load(file)
                self.set_room(rm_ex)
                self.set_room(rm_ex_con)
                
                self.add_player(player)

    # note: if there is a room with the same ID, it will overide it
    # if force=True, it will overide, otherwise it will error
    def set_room(self, data, force=False):
        if type(data) == dict:
            id = data["id"]
            new = db.reference('/rooms/' + str(id))
            if force == True:
                new.set(data)
            else:
                if new.get():
                    raise ValidationErr("there is already a room with this id")
                else:
                    new.set(data)
        else:
            raise TypeError("please serialize the data into a dict")
    
    # literally just the same as set room, but forces overide
    def save_room(self, data):
        self.set_room(data, True)
        
    def get_room(self, id):
        ref = db.reference('/rooms/' + str(id))
        return ref.get()
    
    def add_player(self, data, force=False):
        if type(data) == dict:
            id = data["id"]
            new = db.reference('/users/' + str(id))
            if force == True:
                new.set(data)
            elif new.get():
                raise ValidationErr("there is already a player with this id")
            else:
                new.set(data)
        else:
            raise TypeError("please serialize the data into a dict")
    
    # literally just the same as add_player, but forces overide
    def save_player(self, data):
        self.add_player(data, True)

    def get_player(self, id):
        ref = db.reference('/users/' + str(id))
        return ref.get()
