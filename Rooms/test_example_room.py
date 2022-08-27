import json
from pydoc import describe

f = open("room_example.json", "r")

data = json.load(f)

print(data["name"])

print(f"you enter {data['name']} room")
print(f"you enter a {data['description']}")

if len(data["poi"]["doors"]) > 0:
    print("you see doors:")
    for door in data["poi"]["doors"]:
        print(f" - {door}")

def input_handler(message="> ", dataset=data):
    input_command = input(message)
    input_command = input_command.lower()
    
    if input_command == "exit":
        exit()
    
    if input_command in dataset:
        pass
    # if input_command == "approach":
    #     return "approach"
    if input_command == "inspect":
        desc = dataset["description"]
        print(desc)
    if input_command == "inventory":
        print("inventory")
    else:
        return input_command



def approach(dataset):
    print(dataset["description"])
    
    if "items" in dataset:
        print("you see ", end="")
        length = len(dataset["items"])
        for ind, item in enumerate(dataset["items"]):
            article = "an" if item[0] in "aeiou" else "a"
            if ind == length - 1 and length > 1:
                print(f"and {article} {item}.")
                break
            print(f"{article} {item}, ", end="")
        
        print("what item would you like to inspect?")
        # input_item = input_handler(dataset=dataset)
        input_item = input("> ")
        
        if input_item in dataset["items"]:
            # print(dataset)
            approach(dataset["items"][input_item])
        else:
            print("item not found")
    else:
        print("there are no items here")


if "items"  in data["poi"]:
    print("you see ", end="")
    length = len(data["poi"]["items"])
    for ind, item in enumerate(data["poi"]["items"]):
        article = "an" if item[0] in "aeiou" else "a"
        if ind == length - 1 and length > 1:
            print(f"and {article} {item}.")
            break
        print(f"{article} {item}, ", end="")
        
    print("what item would you like to inspect?")
    # input_item = input_handler()
    # input_item = input_handler(dataset=data["poi"])
    input_item = input("> ")
    
    if input_item in data["poi"]["items"]:
        approach(data["poi"]["items"][input_item])
    else:
        print("item not found")
else:
    print("there are no items in this room")