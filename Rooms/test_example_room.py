import json
# from pydoc import describe
from random import randint

with open("room_example.json", "r") as room_file:
    data = json.load(room_file)

with open("player_data.json", "r") as player_data_file:
    player_data = json.load(player_data_file)

def article(string: str) -> str:
    return "an" if string[0] in "aeiou" else "a"

def describe_poi(dataset: dict):
    if "room" in dataset["class"]:
        print(f"you enter {data['name']} room")
        print(f"you enter a {dataset['descriptions']['main_description']}")

        if len(data["doors"]) > 0:
            print("you see doors:")
            for door in data["doors"]:
                print(f" - {door}")
        
        print_pois(dataset=dataset)

    elif "poi" in dataset:
        print(dataset["descriptions"]["main_description"])
        print_pois(dataset=dataset)

    else:
        print(dataset["descriptions"]["main_description"])
        print("What would you like to do?")


def print_pois(dataset):
    print("You see ", end="")
    length = len(dataset["poi"])
    for ind, item in enumerate(dataset["poi"]):
        if ind == length - 1 and length > 1:
            print(f"and {article(item)} {item}.")
            break
        if length == 1:
            print(f"{article(item)} {item}. ", end="")
            break
        print(f"{article(item)} {item}, ", end="")

    if length == 1:
        print("What would you like to do?")
    else:
        print("What would you like to look at?")

def input_handler(dataset, message="> "):
    input_command = input(message)
    input_command = input_command.lower()

    if "enemy" in dataset["class"]:
        if input_command in ["attack", "fight"]:
            return "attack"

        elif input_command == "run":
            return "run"
        
        else:
            print(f"You can't use {input_command} in combat")
            return

    # misc commands
    if input_command == "help":
        print("available commands: ")
        print(" - exit")
        print(" - help")
        print(" - inspect")
        print(" - inventory")
        input_handler(dataset=dataset)

    elif input_command == "exit":
        exit()
        
    elif input_command == "back":
        increase_cur_noise_level(2)
        if "collectable" in dataset["class"]:
            return
        return "back"

    # take item
    elif input_command in ["take", "grab"]:
        increase_cur_noise_level(5)
        return add_item_to_inventory(dataset)
    
    # approach
    elif input_command in dataset["poi"]:
        increase_cur_noise_level(2)
        return approach(dataset["poi"][input_command])
    
    # approach if there is only 1 poi
    elif len(dataset["poi"]) == 1:
        if input_command in ["look", "inspect", "open", "examine", "go"]:
            increase_cur_noise_level(2)
            return approach(dataset["poi"][list(dataset["poi"])[0]])

    elif input_command == "inspect":
        describe_poi(dataset)
        return input_handler(dataset=dataset)
        
    elif input_command == "inventory":
        increase_cur_noise_level(1)
        print("inventory")
        
    else:
        print('invalid command - type "help" for a list of commands')
        input_handler(dataset=dataset)


def approach(dataset):
    if "poi" in dataset:
        while True: 
            describe_poi(dataset=dataset)
            
            input_handler_return_value = input_handler(dataset=dataset)
            if input_handler_return_value == "back":
                break
            elif input_handler_return_value is not None:
                name = None
                for i in dataset["poi"]:
                    if dataset["poi"][i] == input_handler_return_value:
                        name = i
                        break

                dataset["poi"].pop(name)
                with open("room_example.json", "w") as f:
                    json.dump(data, f)
    else:
        describe_poi(dataset=dataset)
        return input_handler(dataset=dataset)


def add_item_to_inventory(item_data: dict):
    # check if you can take target item
    if "collectable" not in item_data["class"]:
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

def increase_cur_noise_level(volume_increase):
    player_data["cur_noise_level"] += volume_increase
    with open("player_data.json", "w") as f:
        json.dump(player_data, f)

    for i in data["entities"]:
        if int(data["entities"][i]["passive_perception"]) <= int(player_data["cur_noise_level"]):
            combat(data["entities"][i])

def change_player_stat(stat_name, change_amount):
    player_data[stat_name] += change_amount
    with open("player_data.json", "w") as f:
        json.dump(player_data, f)

def combat(enemy_data):
    print(f"The {enemy_data['name']} noticed you!")

    if "ranged" in enemy_data["class"]:
        print(f"With its range the {enemy_data['name']} gets a free attack on you. It {enemy_data['descriptions']['attack_description']}")
        change_player_stat("hp", -enemy_data["dmg"])
        print(f"It hits and deals you {enemy_data['dmg']} hp")
        print(f"It has {player_data['hp']} hp left. ({player_data['hp'] + enemy_data['dmg']} - {enemy_data['dmg']})")

    while True:
        print("What do you do?")
        input_handler_return_value = input_handler(enemy_data)
        if input_handler_return_value == "attack":
            attack_enemy(enemy_data=enemy_data)
        elif input_handler_return_value == "run":
            if randint(1, 10) > 8:
                print("You run away and manage to escape!")
                exit()
                break
            print("You attempt to flee the room, but fail to escape!")
        
        if enemy_data["hp"] <= 0:
            print(f"{enemy_data['name']} has been defeated!")
            break

        print(f"\nthe {enemy_data['name']} attacks. It {enemy_data['descriptions']['attack_description']}")
        change_player_stat("hp", -enemy_data["dmg"])
        print(f"It hits and deals you {enemy_data['dmg']} hp")
        print(f"You have {player_data['hp']} hp left. ({player_data['hp'] + enemy_data['dmg']} - {enemy_data['dmg']})")

def attack_enemy(enemy_data):
    print(player_data["descriptions"]["attack_description"])
    enemy_data["hp"] -= player_data["dmg"]
    with open("room_example.json", "w") as f:
        json.dump(data, f)
    print(f"You hit and deal {player_data['dmg']} to the {enemy_data['name']}.")
    print(f"It has {enemy_data['hp']} hp left. ({enemy_data['hp'] + player_data['dmg']} - {player_data['dmg']})")


approach(data)
