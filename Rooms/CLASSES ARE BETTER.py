from __future__ import annotations
import json
import random

def load_file(file_name: str) -> dict:
    with open(file_name, "r") as f:
        return json.load(f)

def write_to_file(file_name: str, data: dict) -> dict:
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
            child_poi.print_pois(level + 1)

    @property
    def descriptions(self):
        return Descriptions(**self.data["descriptions"])

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

    def add_to_inventory(self, item):
        ...

    def attack_enemy(self, enemy):
        print(self.descriptions.attack)
        old_enemy_hp = enemy.hp
        enemy.hp -= self.dmg
        # enemy.save_data()
        print(f"You hit and deal {self.dmg} to the {enemy.name}.")
        print(f"It has {enemy.hp} hp left. ({old_enemy_hp} - {self.dmg})")

class Item:
    def __init__(self):
        ...


main_room = Poi.get_poi(load_file("room_example.json"))
main_room.print_pois()