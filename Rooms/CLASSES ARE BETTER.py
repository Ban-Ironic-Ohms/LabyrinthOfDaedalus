from __future__ import annotations
import json
import random

class Descriptions:
    def __init__(self, main_description=""):
        self.main = main_description

def load_file(file_name: str) -> dict:
    with open(file_name, "w") as f:
        return json.load(f)

class Room:
    def __init__(self, room_data: dict):
        self.data = room_data

class Poi:
    def __init__(self, poi_data: dict):
        self.data = poi_data

class Entity:
    @staticmethod
    def get_entity(entity_data):
        if "enemy" in entity_data["class"]:
            return Enemy(entity_data)
        else:
            return Entity(entity_data)

    def __init__(self, entity_data):
        self.data = entity_data

    @property
    def name(self):
        return self.data["name"]

    @property
    def entity_class(self):
        return self.data["entity_class"]

    @property
    def descriptions(self):
        return Descriptions(self.data["descriptions"]["main_description"])

class Enemy(Entity):
    class EnemyDescriptions(Descriptions):
        def __init__(self, main_description="", attack_description=""):
            super().__init__(main_description)
            self.attack = attack_description

    @property
    def hp(self):
        return self.data["hp"]

    @property
    def name(self):
        return self.data["name"]

    @property
    def dmg(self):
        return self.data["dmg"]

    @property
    def descriptions(self):
        return self.EnemyDescriptions(
            self.data["descriptions"]["main_description"],
            self.data["descriptions"]["attack_description"]
        )

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
    class PlayerDescriptions(Descriptions):
        def __init__(self, main_description, attack_description):
            super().__init__(main_description)
            self.attack = attack_description

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
        return self.PlayerDescriptions(
            self.data["descriptions"]["main_description"],
            self.data["descriptions"]["attack_description"]
        )

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
