import json

def load_room(room_file_name: str) -> dict:
    with open(f"{room_file_name}.json", "r") as room_file:
        data = json.load(room_file)
    return data

def get_door_description(room_file_name: dict, add_slash_rooms=False) -> str:
    if add_slash_rooms:
        with open(f"Rooms/{room_file_name}.json", "r") as room_file:
            data = json.load(room_file)
        return data["descriptions"]["door_description"]
    else:
        with open(f"{room_file_name}.json", "r") as room_file:
            data = json.load(room_file)
        return data["descriptions"]["door_description"]

# load the room and get the sum of all of the rarity, value, dmg, and hp values of the items in the room
def get_door_value(room_file_name):
    return load_room(room_file_name)["value"]
    