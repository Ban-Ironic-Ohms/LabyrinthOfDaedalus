import json

f = open("room_example.json", "r")

data = json.load(f)

print(data["name"])

print(f"you enter {data['name']} room")
print(f"you enter a {data['description']}")

if len(data["poi"]["doors"]) > 0:
    print("you see doors:")
    for door in data["poi"]["doors"]:
        print(f" - {door}")

        
def approach(approach, dataset):
    print(f"you approach {approach}")
    
    if len(dataset["items"]) > 0:
        print("you see ", end="")
        length = len(dataset["items"])
        for ind, item in enumerate(dataset["items"]):
            article = "an" if item[0] in "aeiou" else "a"
            if ind == length - 1 and length > 1:
                print(f"and {article} {item}.")
                break
            print(f"{article} {item}, ", end="")
        
        print("what item would you like to move to?")
        input_item = input("> ")
        
        if input_item in dataset["items"]:
            approach(input_item, dataset["items"][input_item])
        else:
            print("item not found")            


if len(data["poi"]["items"]) > 0:
    print("you see ", end="")
    length = len(data["poi"]["items"])
    for ind, item in enumerate(data["poi"]["items"]):
        article = "an" if item[0] in "aeiou" else "a"
        if ind == length - 1 and length > 1:
            print(f"and {article} {item}.")
            break
        print(f"{article} {item}, ", end="")
        
    print("what item would you like to move to?")
    input_item = input("> ")
    
    if input_item in data["poi"]["items"]:
        approach(input_item, data["poi"]["items"][input_item])
    else:
        print("item not found")
            