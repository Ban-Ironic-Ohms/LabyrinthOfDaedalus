from __future__ import annotations
from typing import TYPE_CHECKING
import random
from helper_functions import article, pre_print

if TYPE_CHECKING:
    # Anything imported in here may only be used for type hinting.
    from player.player import Player
    from firebase.firebase_interface import Firebase

# LOOK AT THIS!!!!!!
# This is kinda important
# if you want to add more rooms that you want to use, this is where
# you add them by adding the file name to the list. Make sure rooms are in the rooms folder and player are in the player folder

# NOTE: This way is being deprecated in favor of the class based approach
# In order to work with the firebase database, we need to use different functions for rooms and users
# They will live in the parent for each, so just use 
# super().load_room()        super().load_user()
# super().save_room()        super().save_user()
    
class Descriptions:
    DEFAULT = "unimplemented description"

    def __init__(self,
                 main_description=DEFAULT,
                 attack_description=DEFAULT,
                 door_description=DEFAULT,
                 unlock_description=DEFAULT,
                 enter_description=DEFAULT):
        self.main = main_description
        self.attack = attack_description
        self.door = door_description
        self.unlock = unlock_description
        self.enter = enter_description

class Poi:            
    @staticmethod
    def get_poi(poi_data, database=None, parent_poi=None):
        poi_class = poi_data["class"]

        if "room" in poi_class:
            return Room(poi_data, database, poi_data)
        elif "connector" in poi_class:
            return Connector(poi_data, database, parent_poi)
        elif "enemy" in poi_class:
            return Enemy(poi_data, database, parent_poi)
        else:
            return Poi(poi_data, database, parent_poi)

    def __init__(self,
                 poi_data: dict,
                 database: Firebase | None = None,
                 parent_poi: Poi | None = None):
        self.data = poi_data
        self.parent_poi = parent_poi
        self.database = database

        self.child_pois = []
        self.doors = []
        for child_poi_data in self.data["poi"] if "poi" in self.data else []:
            new_child_poi = self.get_poi(child_poi_data, database, self)
            self.child_pois.append(new_child_poi)
            if "door" in child_poi_data["class"]:
                self.doors.append(new_child_poi)
    
    @property
    def name(self):
        return self.data["name"]

    @property
    def cls(self):
        return self.data["class"]

    def print_poi(self, level=0):
        if level == 0:
            pre_print(f"{self.name}:")
        else:
            pre_print(f"{' ' * (level * 3 - 1)}- {self.name}")
        for child_poi in self.child_pois:
            child_poi.print_poi(level + 1)
            
    def print_visible(self):
        if (num_of_child_pois := len(self.child_pois)) > 0:
            pre_print("You see ", end="")
            for ind, item in enumerate(self.child_pois):
                if ind == num_of_child_pois - 1 and num_of_child_pois > 1:
                    pre_print(f"and {article(item.name)} {item.name}.")
                    break
                if num_of_child_pois == 1:
                    pre_print(f"{article(item.name)} {item.name}. ", end="")
                    break
                pre_print(f"{article(item.name)} {item.name}, ", end="")

        if num_of_child_pois <= 1:
            pre_print("What would you like to do?")
        else:
            pre_print("What would you like to look at?")

    @property
    def descriptions(self):
        return Descriptions(**self.data["descriptions"])

    def describe(self):
        pre_print(self.descriptions.main)

    def describe_child_pois(self):
        # TODO: Split doors into two types: Connectors and doors.
        #  Connectors are treated as pois, and transport you to a location when they are used.
        #  Doors are displayed on their own (in describe_doors func), not displayed within the child_poi list.

        # Let the room creator set a custom "use" command to use a poi (i.e. touch, break, light, etc.)

        if (length := len(self.child_pois)) > 0:
            pre_print("You see ", end="")
        for ind, item in enumerate(self.child_pois):
            to_print = "and " if ind == length - 1 and length > 1 else ""
            to_print += f"{article(item.name)} {item.name}"
            to_print += ".\n" if ind == length - 1 else ","
            pre_print(to_print, end="")

        pre_print("What would you like to do?" if length <= 1 else
              "What would you like to look at?")

    def describe_doors(self):
        ...
        # if len(data["doors"]) > 0:
        #     if len(data["doors"]) == 1:
        #         pre_print("you see a door:")
        #     else:
        #         pre_print("you see doors:")
        #     for door in data["doors"]:
        #         pre_print(f" - {door} is {get_door_description(data['doors'][door]['file_name'])}")

    def refresh_child_pois(self):
        self.data["poi"] = [child_poi.data for child_poi in self.child_pois]

    def save_data_to_database(self):
        self.refresh_child_pois()
        if self.parent_poi is None:
            raise TypeError("This poi is not contained under a room")
        else:
            self.parent_poi.save_data_to_database()

    def print_doors(self):
        if not self.doors:
            return
        if len(self.doors) == 1:
            a = "you see a door:"
        else:
            a = "you see doors:"
        pre_print(a)
        for door in self.doors:
            pre_print(door.get_display())

        pre_print()

class Room(Poi):
    @property
    def id(self):
        return self.data["id"]

    # load and save functions to firebase
    @staticmethod
    def load_data_from_database(database: Firebase, room_id) -> dict:
        return database.get_room(room_id)

    def save_data_to_database(self):
        self.refresh_child_pois()
        self.database.set_room(self.data)
        
    def print_room(self):
        pre_print(f"{self.name}:")

    def get_room_value(self):
        """Returns the value of the room based on all the rarity, value, dmg, and hp values of the items in the room"""
        return self.data["value"]
            
class Connector(Poi):
    @property
    def id(self):
        return self.data["id"]

    @property
    def descriptions(self):
        default_descriptions = {
            "unlock": "Unlock",
            "enter": "Enter"
        } if "door" in self.cls else {}
        # Unpack default_descriptions first so that it is overridden by any descriptions in data
        return Descriptions(**{**default_descriptions, **self.data["descriptions"]})

    def get_door_desc(self):
        if self.database:
            return self.database.get_room(self.id)["descriptions"]["door_description"]
        else:
            return "a basic door"

    def get_display(self):
        # print name, id, and door description
        return f"{self.name} - {self.get_door_desc()}"

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

    def combat(self, player: Player, input_handler):
        pre_print(f"The {self.name} noticed you!")

        if "ranged" in self.cls:
            pre_print(
                f"With its range the {self.name} gets a free attack on you. It {self.descriptions.attack}")
            player.hp -= self.dmg
            pre_print(f"It hits and deals you {self.dmg} hp")
            pre_print(f"It has {player.hp} hp left. ({player.hp + self.dmg} - {self.dmg})")

        while True:
            pre_print("What do you do?")
            input_handler_return_value = input_handler(self, player)
            if input_handler_return_value == "attack":
                player.attack_enemy(self)
            elif input_handler_return_value in ["run", "flee", "escape", "back", "back down", "back away", "retreat"]:
                if random.randint(1, 10) > 8:
                    pre_print("You run away and manage to escape!")
                    exit()
                    break
                pre_print("You attempt to flee the room, but fail to escape!")

            if self.hp <= 0:
                pre_print(f"{self.name} has been defeated!")
                break

            pre_print(f"\nthe {self.name} attacks. It {self.descriptions.attack}")
            prev_player_hp = player.hp
            player.hp -= self.dmg
            pre_print(f"It hits and deals you {self.dmg} hp")
            pre_print(f"You have {player.hp} hp left. ({prev_player_hp} - {self.dmg})")
