import json
from pydoc import describe

inventory = []

f = open("room_example.json", "r")
data = json.load(f)

inv = open("inventory.json", "r")
inventory = json.load(inv)

print(f"you enter {data['name']} room")
print(f"you enter a {data['description']}")

if len(data["doors"]) > 0:
    print("you see doors:")
    for door in data["doors"]:
        print(f" - {door}")

# todo doors

def get_poi(dataset):
    if "poi" in dataset:
        print("you see ", end="")
        length = len(dataset["poi"])
        for ind, item in enumerate(dataset["poi"]):
            if ind == length - 1 and length > 1:
                print(f"and {article(item)} {item}.")
                break
            print(f"{article(item)} {item}, ", end="")
        print("what item would you like to inspect?")

def input_handler(dataset, message="> "):
    input_command = input(message)
    input_command = input_command.lower()

        
    # misc commands
    if input_command == "exit":
        exit()
        
    elif input_command == "back":
        return "back"

    elif input_command == "help":
        print("available commands: ")
        print(" - exit")
        print(" - help")
        print(" - inspect")
        print(" - inventory")
        input_handler(dataset=dataset)

    elif input_command in ["take", "grab"]:
        # inventory.append(dataset)
        if dataset["class"] != "collectable":
            print(f"You can't put {article(dataset['name'])} {dataset['name']} in your inventory!")
            return
        name = dataset["name"]
        print(f"You have aquired {article(name)} {name}")
        
        # add to inventory
        inventory[name] = dataset
        
        # remove from room
        # TODO
        
        with open("inventory.json", "w") as f:
            json.dump(inventory, f)

        return dataset
    
    # approach
    elif input_command in dataset["poi"]:
        return approach(dataset["poi"][input_command])
        

    elif input_command == "inspect":
        desc = dataset["description"]
        print(f"you see {desc}")
        
        get_poi(dataset)
       
        return input_handler(dataset=dataset)
        
    elif input_command == "inventory":
        print("inventory")
        
    else:
        print('invalid command - type "help" for a list of commands')
        input_handler(dataset=dataset)


def article(string):
    return "an" if string[0] in "aeiou" else "a"

def approach(dataset):
    print(dataset["description"])
    
    if "poi" in dataset:
        while True: 
            print("you see ", end="")
            length = len(dataset["poi"])
            for ind, item in enumerate(dataset["poi"]):
                if ind == length - 1 and length > 1:
                    print(f"and {article(item)} {item}.")
                    break
                print(f"{article(item)} {item}, ", end="")
            print("what item would you like to inspect?")
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
        print("What would you like to do?")
        return input_handler(dataset=dataset)


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