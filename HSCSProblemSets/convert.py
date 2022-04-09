import colorama
from colorama import Fore, Style

while True:
    num_to_convert = input("What number do you want to convert?  ")
    highest_power = 8
    try:
        num_to_convert = int(num_to_convert)
    except ValueError:
        print("That was not a number, please try again")
        continue
    if num_to_convert < 0:
        print("Must be a positive number")
        continue
    elif num_to_convert > 2**highest_power:
        print("Must be a number smaller than {}".format(2**highest_power))
        continue

    binary_num = "0"
    converted = False

    if num_to_convert > 0:
        next_power = highest_power
        for i in range(0,highest_power+1):
            if converted:
                binary_num += "0"
            else:
                if (num_to_convert // 2**next_power) % 2 == 1:
                    binary_num += "1"
                else:
                    binary_num += "0"
                    pass
                next_power -= 1



    print("\n{} in binary is {}\n".format(Fore.GREEN + str(num_to_convert) + Style.RESET_ALL, Fore.BLUE + binary_num + Style.RESET_ALL))