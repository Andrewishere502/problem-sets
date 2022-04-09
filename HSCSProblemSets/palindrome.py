import re

phrase = input("Please input a phrase:  ").strip().lower()

for char in phrase:
    whitespace = re.match(r"\s", char)  # search for whitespace
    if whitespace != None:
        # Replace whitespace with nothing
        phrase = phrase.replace(whitespace.string, "")

if phrase[::-1] == phrase:  # match phrase to phrase backwards
    print("{} is a palindrome".format(phrase))
else:
    print("{} is not a palindrome".format(phrase))
