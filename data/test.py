import re

string1 = "the up shot is"
string2 = "but we struggle to make out what we're trying to say"
key = " shot+\n"

strings = [string1, string2]

pattern = re.compile(key.rstrip(), re.IGNORECASE)
for w in strings:
    if bool(pattern.search(w)):
        print("yay")
    else:
        print("nay")
