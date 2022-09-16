# Thanks to github.com/mdrkb for this template. I could not find documentation for this
from xml.dom import ValidationErr
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import os

# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebase/firebase-keys.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com/'
})
    
class Firebase:
    def __init__(self,
                 base_rooms=("room_example.json", "room_example_connector.json"),
                 base_players=("player_data.json",),
                 reset=False, base=True):
        if reset:
            with open("firebase/init.json") as file:
                data = json.load(file)

            ref = db.reference('/')
            ref.set(data)
            
            if base:
                rooms = []
                for i in base_rooms:
                    with open('rooms/' + i) as file:
                        rooms.append(json.load(file))
                players = []
                for i in base_players:
                    with open('player/' + i) as file:
                        players.append(json.load(file))
                
                for i in rooms:
                    self.set_room(i)
                for i in players:
                    self.set_player(i)

    # note: if there is a room with the same ID, it will override it if force=True, otherwise an error will be thrown
    @staticmethod
    def set_room(data, force=False):
        if type(data) == dict:
            room_id = data["id"]
            new = db.reference('/rooms/' + str(room_id))
            if force:
                new.set(data)
            else:
                if new.get():
                    raise ValidationErr("there is already a room with this id")
                else:
                    new.set(data)
        else:
            raise TypeError("please serialize the data into a dict")

    def save_room(self, data):
        """Calls set_room, but forces override"""
        self.set_room(data, True)

    @staticmethod
    def get_room(room_id):
        ref = db.reference('/rooms/' + str(room_id))
        return ref.get()

    @staticmethod
    def set_player(data, force=False):
        if type(data) == dict:
            player_id = data["id"]
            new = db.reference('/users/' + str(player_id))
            if force:
                new.set(data)
            elif new.get():
                raise ValidationErr("there is already a player with this id")
            else:
                new.set(data)
        else:
            raise TypeError("please serialize the data into a dict")

    def save_player(self, data):
        """Calls set_player, but forces override"""
        self.set_player(data, True)

    @staticmethod
    def get_player(player_id):
        ref = db.reference('/users/' + str(player_id))
        return ref.get()
