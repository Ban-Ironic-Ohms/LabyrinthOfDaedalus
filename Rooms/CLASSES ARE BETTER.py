from __future__ import annotations
import re
import sys
sys.path.append("./")

import json
import random
from helper_functions import article
from firebase_interface import Firebase


# LOOK AT THIS!!!!!!
# This is kinda important
# if you want to add more rooms that you want to use, this is where
# you add them by adding the file name to the list. Make sure rooms are in the Rooms folder and player are in the Players folder
base_rooms = ["room_example.json", "room_example_connector.json"]
base_players = ["player_data.json"]
database = Firebase(base_rooms=base_rooms, base_players=base_players, reset=True)


# NOTE: This way is being deprecated in favor of the class based approach
# In order to work with the firebase database, we need to use different functions for rooms and users
# They will live in the parent for each, so just use 
# super().load_room()        super().load_user()
# super().save_room()        super().save_user()
"""
def load_file(file_name: str) -> dict:
    with open(file_name, "r") as f:
        return json.load(f)

def write_to_file(file_name: str, data: dict):
    with open(file_name, "w") as f:
        return json.dump(data, f)
"""

def input_handler(dataset, message: str = "> "):
    input_command = input(message)
    input_command = input_command.lower()
    
    # misc commands
    if input_command == "help":
        print("available commands: ")
        print(" - exit")
        print(" - help")
        print(" - inspect")
        print(" - inventory")
        print(" - door #")
        input_handler(dataset=dataset)

    elif input_command == "exit":
        exit()

    # this needs to be changed to print just the visible items - not sure what fnc to use
    elif input_command in ["inspect", "info", "look"]:
        dataset.print_visable()
        
    elif input_command in [child_poi_but_i_need_the_name.name for child_poi_but_i_need_the_name in dataset.child_pois]:
        for child_poi_that_we_might_want in dataset.child_pois:
            if child_poi_that_we_might_want.name == input_command:
                player.approach(child_poi_that_we_might_want)
                return

    # todo back
    
    # todo go to doors
    elif input_command in [door.name for door in dataset.doors]:
        for door in dataset.doors:
            if door.name == input_command:
                player.approach(Room(door.id))
    
    
    elif input_command in dataset.child_pois:
        print(dataset.child_pois[input_command].description)
        input_handler(dataset=dataset.child_pois[input_command])

    else:
        print(dataset.child_pois)
        return input_command
    
class Descriptions:
    DEFAULT = "unimplemented description"

    def __init__(self, main_description=DEFAULT, attack_description=DEFAULT, door_description=DEFAULT):
        self.main = main_description
        self.attack = attack_description
        self.door = door_description

class Poi:            
    @staticmethod
    def get_poi(poi_data, parent_poi=None):
        if "room" in poi_data["class"]:
            return Room(poi_data, parent_poi)
        if "enemy" in poi_data["class"]:
            return Enemy(poi_data, parent_poi)
        else:
            return Entity(poi_data, parent_poi)

    def __init__(self, poi_data: dict, parent_poi: Poi | None = None):
        self.data = poi_data
        self.parent_poi = parent_poi

        if "poi" in self.data:
            self.child_pois = [self.get_poi(child_poi_data, parent_poi=self) for
                               child_poi_data in self.data["poi"]]
        else:
            self.child_pois = []

    # load and save functions to firebase
    def load_room(self, id) -> dict:
        return database.get_room(id)
    
    def save_room(self, id, data: dict):
        database.set_room(id, data)
    
    @property
    def name(self):
        return self.data["name"]

    @property
    def cls(self):
        return self.data["class"]

    def print_poi(self, level=0):
        if level == 0:
            print(f"{self.name}:")
        else:
            print(f"{' ' * (level * 3 - 1)}- {self.name}")
        for child_poi in self.child_pois:
            child_poi.print_poi(level + 1)
            
    def print_visable(self, level=0):
        if (length := len(self.child_pois)) > 0:
            print("You see ", end="")
            for ind, item in enumerate(self.child_pois):
                if ind == length - 1 and length > 1:
                    print(f"and {article(item.name)} {item.name}.")
                    break
                if length == 1:
                    print(f"{article(item.name)} {item.name}. ", end="")
                    break
                print(f"{article(item.name)} {item.name}, ", end="")

        if length == 1:
            print("What would you like to do?")
        else:
            print("What would you like to look at?")


    @property
    def descriptions(self):
        return Descriptions(**self.data["descriptions"])

    def describe(self):
        print(self.descriptions.main)

    def describe_child_pois(self):
        # TODO: Split doors into two types: Connectors and doors.
        #  Connectors are treated as pois, and transport you to a location when they are used.
        #  Doors are displayed on their own (in describe_doors func), not displayed within the child_poi list.

        # Let the room creator set a custom "use" command to use a poi (i.e. touch, break, light, etc.)

        if (length := len(self.child_pois)) > 0:
            print("You see ", end="")
        for ind, item in enumerate(self.child_pois):
            to_print = "and " if ind == length - 1 and length > 1 else ""
            to_print += f"{article(item)} {item}"
            to_print += ".\n" if ind == length - 1 else ","
            print(to_print, end="")

        print("What would you like to do?" if length <= 1 else
              "What would you like to look at?")

    def describe_doors(self):
        ...
        # if len(data["doors"]) > 0:
        #     if len(data["doors"]) == 1:
        #         print("you see a door:")
        #     else:
        #         print("you see doors:")
        #     for door in data["doors"]:
        #         print(f" - {door} is {get_door_description(data['doors'][door]['file_name'])}")

    def refresh_child_pois(self):
        self.data["poi"] = [child_poi.data for child_poi in self.child_pois]

    def save_data(self):
        self.refresh_child_pois()
        if self.parent_poi is None:
            raise TypeError("This poi is not contained within a room")
        else:
            self.parent_poi.save_data()

class Room(Poi):
    def __init__(self, id, room_data=None, **kwargs):
        if room_data is None:
            room_data = super().load_room(id)
        self.id = id
        self.doors = []
        for door in room_data["doors"]:
            self.doors.append(Door(door, room_data["doors"][door]["id"]))
        super().__init__(room_data, **kwargs)
        
    def print_doors(self):
        for door in self.doors:
            print(door)
                
    def save_data(self):
        self.refresh_child_pois()
        super().save_room(self.id, self.data)
        
    def print_room(self):
        print(f"{self.name}:")

            
class Door(Poi):
    def __init__(self, name, id):
        self._name = name
        self._id = id
    
    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    def get_door_desc(self):
        return database.get_room(self._id)["descriptions"]["door_description"]
    
    def __str__(self):
        # print name, id, and door description
        return(f"{self._name} - {self.get_door_desc()}")

class Entity(Poi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Enemy(Entity):

    @property
    def hp(self):
        return self.data["hp"]

    @hp.setter
    def hp(self, value):
        self.data["hp"] = value

    @property
    def name(self):
        return self.data["name"]

    @property
    def dmg(self):
        return self.data["dmg"]

    def combat(self, player: Player):
        print(f"The {self.name} noticed you!")

        if "ranged" in self.cls:
            print(
                f"With its range the {self.name} gets a free attack on you. It {self.descriptions.attack}")
            player.hp -= self.dmg
            print(f"It hits and deals you {self.dmg} hp")
            print(f"It has {player.hp} hp left. ({player.hp + self.dmg} - {self.dmg})")

        while True:
            print("What do you do?")
            input_handler_return_value = input_handler(self)
            if input_handler_return_value == "attack":
                player.attack_enemy(self)
            elif input_handler_return_value in ["run", "flee", "escape", "back", "back down", "back away", "retreat"]:
                if random.randint(1, 10) > 8:
                    print("You run away and manage to escape!")
                    exit()
                    break
                print("You attempt to flee the room, but fail to escape!")

            if self.hp <= 0:
                print(f"{self.name} has been defeated!")
                break

            print(f"\nthe {self.name} attacks. It {self.descriptions.attack}")
            prev_player_hp = player.hp
            player.hp -= self.dmg
            print(f"It hits and deals you {self.dmg} hp")
            print(f"You have {player.hp} hp left. ({prev_player_hp} - {self.dmg})")

class Player:
    def __init__(self, id, player_data: dict = None):
        self.id = id
        if player_data:
            self.data = player_data
        else:
            self.data = self.load_player(id)

    # load and save functions to firebase
    def load_player(self, id):
        return database.get_player(id)
    
    def save_player(self, id):
        database.save_player(id, self.data)
    
    @property
    def inventory(self):
        return self.data["inventory"]

    @inventory.setter
    def inventory(self, value):
        self.data["inventory"] = value

    @property
    def hp(self):
        return self.data["hp"]

    @hp.setter
    def hp(self, value):
        self.data["hp"] = value

    @property
    def dmg(self):
        return self.data["dmg"]

    @dmg.setter
    def dmg(self, value):
        self.data["dmg"] = value

    @property
    def descriptions(self):
        return Descriptions(**self.data["descriptions"])

    @property
    def noise_level(self):
        return self.data["cur_noise_level"]

    @noise_level.setter
    def noise_level(self, value):
        self.data["cur_noise_level"] = value

    # TODO: Don't use dictionaries to store child_pois in json. We have no use for the keys,
    #  and duplicate keys could be really bad. Starts to get rly bad when you transferring items between rooms.

    def add_to_inventory(self, item: Poi):
        name = item.name

        # check if you can take target item
        if "item" not in item.cls:
            print(f"You can't put {article(name)} {name} in your inventory!")
            return None

        # tell player they got the item
        print(f"You have acquired {article(name)} {name}")

        # add to inventory
        self.inventory.append(item.data)

    def attack_enemy(self, enemy: Enemy):
        print(self.descriptions.attack)
        old_enemy_hp = enemy.hp
        enemy.hp -= self.dmg
        # enemy.save_data()
        print(f"You hit and deal {self.dmg} to the {enemy.name}.")
        print(f"It has {enemy.hp} hp left. ({old_enemy_hp} - {self.dmg})")
        
    def approach(self, target: Poi):
        
        if type(target) == Room:
            target.print_doors()
        
        print(f"You approach {article(target.name)} {target.name}")
        target.print_visable()

        if len(target.child_pois) > 0:
            while True:                
                input_handler_return_value = input_handler(target)

    def save_data(self):
        self.save_player(self.id, self.data)


main_room = Room("00000000000000000000000000000001")

player = Player("0000000000000000")

player.approach(main_room)

main_room.save_data()
