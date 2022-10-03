from rooms.poi import Room
from player.player import Player
from firebase.firebase_interface import Firebase
from helper_functions import pre_print


def input_handler(current_poi, player: Player, message: str = "> "):
    input_command = input(message)
    input_command = input_command.lower()

    # misc commands
    if input_command == "help":
        pre_print("available commands: ")
        pre_print(" - exit")
        pre_print(" - help")
        pre_print(" - inspect")
        pre_print(" - inventory")
        pre_print(" - door #")
        input_handler(current_poi, player)

    elif input_command == "exit":
        exit()

    # this needs to be changed to pre_print just the visible items - not sure what fnc to use
    elif input_command in ["inspect", "info", "look"]:
        current_poi.pre_print_visible()

    elif input_command in [child_poi.name for child_poi in current_poi.child_pois]:
        for child_poi in current_poi.child_pois:
            if child_poi.name == input_command:
                player.approach(child_poi, input_handler)
                return

    # todo back

    # todo go to doors
    elif input_command in [door.name for door in current_poi.doors]:
        for door in current_poi.doors:
            if door.name == input_command:
                player.approach(Room(door.id))

    elif input_command in current_poi.child_pois:
        pre_print(current_poi.child_pois[input_command].description)
        input_handler(current_poi.child_pois[input_command], player)

    else:
        pre_print("Invalid command - Type help for valid commands")
        return input_command

def main():
    base_rooms = ["room_example.json", "room_example_connector.json"]
    base_players = ["player_data.json"]
    database = Firebase(base_rooms=base_rooms, base_players=base_players, reset=True)

    main_room = Room(Room.load_data_from_database(database, "00000000000000000000000000000001"), database)

    player = Player(Player.load_data_from_database(database, "0000000000000000"), database)

    player.approach(main_room, input_handler)

    # main_room.save_data_to_database()


if __name__ == "__main__":
    Firebase.reset_message()
    main()
