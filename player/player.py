from __future__ import annotations
from typing import TYPE_CHECKING
from helper_functions import article

if TYPE_CHECKING:
    from firebase.firebase_interface import Firebase
    from rooms.poi import Poi, Enemy

class Descriptions:
    DEFAULT = "unimplemented description"

    def __init__(self,
                 main_description=DEFAULT,
                 attack_description=DEFAULT):
        self.main = main_description
        self.attack = attack_description

class Player:
    def __init__(self, player_data: dict, database: Firebase):
        self.data = player_data
        self.database = database

    # load and save functions to firebase
    @staticmethod
    def load_data_from_database(database: Firebase, player_id):
        return database.get_player(player_id)

    def save_data_to_database(self):
        self.database.save_player(self.data)

    @property
    def inventory(self):
        return self.data["inventory"]

    @property
    def id(self):
        return self.data["id"]

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
        # enemy.save_data_to_database()
        print(f"You hit and deal {self.dmg} to the {enemy.name}.")
        print(f"It has {enemy.hp} hp left. ({old_enemy_hp} - {self.dmg})")

    def approach(self, target: Poi, input_handler):
        # if isinstance(target, Room):  # If you ever need to check what type of POI target is, feel free but talk to me after -owen
        target.print_doors()

        print(f"You approach {article(target.name)} {target.name}")
        target.print_visible()

        if len(target.child_pois) > 0:
            while True:
                _input_handler_return_value = input_handler(target, self)
