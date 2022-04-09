def is_odd(num):
    return num % 2


while True:
    find_middle_of = input("Enter something!\n> ")

    if is_odd(len(find_middle_of)):
        middle_letter_index = int(len(find_middle_of) / 2)
        print(find_middle_of[middle_letter_index])
    else:
        middle_letter_index_1 = int(len(find_middle_of) / 2) - 1
        middle_letter_index_2 = int(len(find_middle_of) / 2)
        print(find_middle_of[middle_letter_index_1] + find_middle_of[middle_letter_index_2])
