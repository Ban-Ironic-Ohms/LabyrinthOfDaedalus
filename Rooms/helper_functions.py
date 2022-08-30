def article(string: str) -> str:
    return "an" if string[0] in "aeiou" else "a"