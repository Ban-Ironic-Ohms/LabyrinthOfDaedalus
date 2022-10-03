from firebase.firebase_interface import Firebase

def article(string: str) -> str:
    return "an" if string[0] in "aeiou" else "a"

def pre_print(input="", end="\n"):
    newline = False
    if end != "":
        newline = True
    
    Firebase.new_message(input, newline)
    print(input, end=end)