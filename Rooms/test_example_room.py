import json
from pydoc import describe

f = open("room_example.json", "r")

data = json.load(f)

print(data["name"])

print(f"you enter {data['name']} room")
print(f"you enter a {data['description']}")

if len(data["doors"]) > 0:
    print("you see doors:")
    for door in data["doors"]:
        print(f" - {door}")

def input_handler(dataset, message="> "):
    input_command = input(message)
    input_command = input_command.lower()
    
    # misc commands
    if input_command == "exit":
        exit()
        
    if input_command == "help":
        print("available commands: ")
        print(" - exit")
        print(" - help")
        # print(" - inspect")
        input_handler(dataset=dataset)
    
    # approach
    if input_command in dataset:
        approach(dataset[input_command])

    # if input_command == "inspect":
    #     desc = dataset["description"]
    #     print(desc)
        
    # if input_command == "inventory":
    #     print("inventory")
        
    else:
        print('invalid command - type "help" for a list of commands')
        input_handler(dataset=dataset)
        
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
        input_handler(dataset=dataset["poi"])

    else:
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
    input_handler(dataset=data["poi"])

else:
    print("there are no items in this room")