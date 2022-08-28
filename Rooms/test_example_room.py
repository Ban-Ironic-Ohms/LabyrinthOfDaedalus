import json
from pydoc import describe

f = open("room_example.json", "r")
data = json.load(f)

f_pd = open("player_data.json", "r")
player_data = json.load(f_pd)

# print(f"you enter {data['name']} room")
# print(f"you enter a {data['description']}")

# if len(data["doors"]) > 0:
#     print("you see doors:")
#     for door in data["doors"]:
#         print(f" - {door}")

# todo doors

def article(string):
    return "an" if string[0] in "aeiou" else "a"

def discribe_poi(dataset):
    if dataset["class"] == "room":
        print(f"you enter {data['name']} room")
        print(f"you enter a {data['description']}")

        if len(data["doors"]) > 0:
            print("you see doors:")
            for door in data["doors"]:
                print(f" - {door}")
        
        print_pois(dataset=dataset)

    elif "poi" in dataset:
        print(dataset["description"])
        print_pois(dataset=dataset)

    else:
        print(dataset["description"])
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

        
    # misc commands
    if input_command == "exit":
        exit()
        
    elif input_command == "back":
        if dataset["class"] == "collectable":
            return
        return "back"

    elif input_command == "help":
        print("available commands: ")
        print(" - exit")
        print(" - help")
        print(" - inspect")
        print(" - inventory")
        input_handler(dataset=dataset)

    elif input_command in ["take", "grab"]:
        return add_item_to_inventory(dataset)
    
    # approach
    elif input_command in dataset["poi"]:
        return approach(dataset["poi"][input_command])
        

    elif input_command == "inspect":
        discribe_poi(dataset)
        return input_handler(dataset=dataset)
        
    elif input_command == "inventory":
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
    if dataset["class"] != "collectable":
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

def combat():
    pass

approach(data)



# if "poi" in data:
#     print("you see ", end="")
#     length = len(data["poi"])
#     for ind, item in enumerate(data["poi"]):
#         article = "an" if item[0] in "aeiou" else "a"
#         if ind == length - 1 and length > 1:
#             print(f"and {article} {item}.")
#             break
#         print(f"{article} {item}, ", end="")
        
#     print("what item would you like to inspect?")
#     input_handler(dataset=data)

# else:
#     print("there are no items in this room")