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

    @property
    def name(self):
        return self.data["name"]

    def __init__(self, poi_data: dict, parent_poi: Poi | None = None):
        self.data = poi_data
        self.parent_poi = parent_poi

        if "poi" in self.data:
            self.child_pois = [self.get_poi(child_poi_data) for
                               child_poi_tag, child_poi_data in self.data["poi"].items()]
        else:
            self.child_pois = []

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

class Room(Poi):
    ...

class Entity(Poi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def entity_class(self):
        return self.data["entity_class"]

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

        if "ranged" in self.entity_class:
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

    @property
    def inventory(self):
        return self.data["inventory"]

    def add_to_inventory(self, item: Item):
        # check if you can take target item
        if "collectible" not in item_data["class"]:
            print(f"You can't put {article(item_data['name'])} {item_data['name']} in your inventory!")
            return None

        # tell player they got the item
        name = item_data["name"]
        print(f"You have acquired {article(name)} {name}")

        # add to inventory
        player_data["inventory"][name] = item_data

        # save to player data file
        with open("player_data.json", "w") as f:
            json.dump(player_data, f)

        return item_data

    def attack_enemy(self, enemy: Enemy):
        print(self.descriptions.attack)
        old_enemy_hp = enemy.hp
        enemy.hp -= self.dmg
        # enemy.save_data()
        print(f"You hit and deal {self.dmg} to the {enemy.name}.")
        print(f"It has {enemy.hp} hp left. ({old_enemy_hp} - {self.dmg})")

class Item:
    # TODO: Is this a poi? No, right? Or else you shouldn't
    def __init__(self, item_data):
        self.data = item_data

main_room = Room(load_file("room_example.json"))
