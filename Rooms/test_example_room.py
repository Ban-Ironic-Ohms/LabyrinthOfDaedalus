import json
from pydoc import describe

f = open("room_example.json", "r")
data = json.load(f)

f_pd = open("player_data.json", "r")
player_data = json.load(f_pd)

def article(string):
    return "an" if string[0] in "aeiou" else "a"

def discribe_poi(dataset):
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
        if input_command == "attack":
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
        if  "collectable" in dataset["class"]:
            return
        return "back"

    elif input_command in ["take", "grab"]:
        increase_cur_noise_level(5)
        return add_item_to_inventory(dataset)
    
    # approach
    elif input_command in dataset["poi"]:
        increase_cur_noise_level(2)
        return approach(dataset["poi"][input_command])
        

    elif input_command == "inspect":
        discribe_poi(dataset)
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
            discribe_poi(dataset=dataset)
            
            input_handler_return_value = input_handler(dataset=dataset)
            if input_handler_return_value == "back":
                break
            elif input_handler_return_value != None:
                for i in dataset["poi"]:
                    if dataset["poi"][i] == input_handler_return_value:
                        name = i
                        
                dataset["poi"].pop(name)
                with open("room_example.json", "w") as f:
                    json.dump(data, f)
    else:
        discribe_poi(dataset=dataset)
        return input_handler(dataset=dataset)


def add_item_to_inventory(dataset):
    #check if you can take target item
    if "collectable" not in dataset["class"]:
        print(f"You can't put {article(dataset['name'])} {dataset['name']} in your inventory!")
        return None
    
    #tell player they got the item
    name = dataset["name"]
    print(f"You have aquired {article(name)} {name}")
    
    # add to inventory
    player_data["inventory"][name] = dataset
    
    # save to player data file
    with open("player_data.json", "w") as f:
        json.dump(player_data, f)

    return dataset

def increase_cur_noise_level(volume_increase):
    player_data["cur_noise_level"] += volume_increase
    with open("player_data.json", "w") as f:
        json.dump(player_data, f)

    for i in data["entities"]:
        if (int(data["entities"][i]["passive_perception"]) <= int(player_data["cur_noise_level"])):
            combat(data["entities"][i])

def change_player_stat(stat_name, change_amount):
    player_data[stat_name] += change_amount
    with open("player_data.json", "w") as f:
        json.dump(player_data, f)


def combat(enemy_data):
    print(f"The {enemy_data['name']} noticed you. It attacks!")

    if "ranged" in enemy_data["class"]:
        print(f"With its range the {enemy_data['name']} gets a free attack on you. It {enemy_data['descriptions']['attack_description']}")
        change_player_stat("hp", -enemy_data["dmg"])

    while True:
        print("What do you do?")
        input_handler_return_value = input_handler(enemy_data)
        if input_handler_return_value == "attack":
            attack_enemy(enemy_data=enemy_data)
            
        if enemy_data["hp"] <= 0:
            print(f"{enemy_data['name']} has been defeated!")
            break

def attack_enemy(enemy_data):
    print(player_data["descriptions"]["attack_description"])
    enemy_data["hp"] -= player_data["dmg"]
    with open("data.json", "w") as f:
        json.dump(data, f)
    print(f"You hit and deal {player_data['dmg']} to the {enemy_data['name']}.")
    print(f"It has {enemy_data['hp']} hp left. ({enemy_data['hp'] + player_data['dmg']} - {player_data['dmg']})")

approach(data)
