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
            article = "an" if item[0] in "aeiou" else "a"
            if ind == length - 1 and length > 1:
                print(f"and {article} {item}.")
                break
            print(f"{article} {item}, ", end="")
        print("what item would you like to inspect?")

def input_handler(dataset, message="> "):
    input_command = input(message)
    input_command = input_command.lower()
    
    if input_command == "test":
        for idx, obj in enumerate(inventory):
            if obj['id'] == 2:
                inventory.pop(idx)
        inv = open("inventory.json", "w")
        inv.write(json.dumps("inventory.json"))

    # misc commands
    if input_command == "exit":
        exit()
        
    if input_command == "back":
        pass

    if input_command == "help":
        print("available commands: ")
        print(" - exit")
        print(" - help")
        # print(" - inspect")
        input_handler(dataset=dataset)

    if input_command in ["take", "grab"]:
        inventory.append(dataset)
        name = dataset["name"]
        article = "an" if name[0] in "aeiou" else "a"
        print(f"You have aquired {article} {name}")
    
    # approach
    if input_command in dataset["poi"]:
        approach(dataset["poi"][input_command])

    if input_command == "inspect":
        desc = dataset["description"]
        print(f"you see {desc}")
        
        get_poi(dataset)
       
        return input_handler(dataset=dataset)
        
    # if input_command == "inventory":
    #     print("inventory")
        
    else:
        print('invalid command - type "help" for a list of commands')
        input_handler(dataset=dataset)

def remove_json_entry(dataset):
    pass

def approach(dataset):
    print(dataset["description"])
    
    if "poi" in dataset:
        print("you see ", end="")
        length = len(dataset["poi"])
        for ind, item in enumerate(dataset["poi"]):
            article = "an" if item[0] in "aeiou" else "a"
            if ind == length - 1 and length > 1:
                print(f"and {article} {item}.")
                break
            print(f"{article} {item}, ", end="")
        
        print("what item would you like to inspect?")
        input_handler(dataset=dataset)

    else:
        print("What would you like to do?")
        input_handler(dataset=dataset);
        print("there are no items here")


if "poi" in data:
    print("you see ", end="")
    length = len(data["poi"])
    for ind, item in enumerate(data["poi"]):
        article = "an" if item[0] in "aeiou" else "a"
        if ind == length - 1 and length > 1:
            print(f"and {article} {item}.")
            break
        print(f"{article} {item}, ", end="")
        
    print("what item would you like to inspect?")
    input_handler(dataset=data)

else:
    print("there are no items in this room")