sequence = input()

current_char = sequence[0]
length = 1
max_length = -1
for char in sequence[1:]:
    if char == current_char:
        length += 1
    else:
        current_char = char
        if length > max_length:
            max_length = length
        length = 1

if length > max_length:
    print(length)
else:
    print(max_length)
