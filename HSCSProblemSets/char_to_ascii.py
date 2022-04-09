def to_ascii(o):
    num = ord(o)
    if num not in range(128):
        raise ValueError("{} is not an ascii character".format(o))
    return num


phrase = input("Please enter a phrase:  ")
ascii_phrase = [str(to_ascii(char)) for char in phrase]
binary_phrase = [str(bin(to_ascii(char))) for char in phrase]

print("Plain text:  ", end="")
print(" - ".join([char for char in phrase]))

print("Ascii:  ", end="")
print(" - ".join(ascii_phrase))

print("Binary:  ", end="")
print(" - ".join(binary_phrase))
