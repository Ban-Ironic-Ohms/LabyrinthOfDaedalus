from __future__ import annotations
import json
import random
from helper_functions import article

def load_file(file_name: str) -> dict:
    with open(file_name, "r") as f:
        return json.load(f)

def write_to_file(file_name: str, data: dict):
    with open(file_name, "w") as f:
        return json.dump(data, f)

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
    def __init__(self, data_file_name, room_data=None, **kwargs):
        if room_data is None:
            room_data = load_file(data_file_name)
        self.data_file_name = data_file_name
        super().__init__(room_data, **kwargs)

    def save_data(self):
        self.refresh_child_pois()
        write_to_file(self.data_file_name, self.data)

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
    def __init__(self, player_data: dict):
        self.data = player_data

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


main_room = Room("room_example.json")

main_room.save_data()
