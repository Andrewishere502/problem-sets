factorials_up_to = input("Factorials will from 0 to ")

factorials_up_to = int(factorials_up_to)  # might get error

factorial_answers = {}

for get_factorial in range(0, factorials_up_to+1):
    factorial = get_factorial
    for num in range(1, get_factorial):
        factorial = factorial * num
    factorial_answers.update({get_factorial: factorial})

# print(factorial_answers)

file_root = "/Users/21berntson_a/Documents/Programming/Problem Sets PY/factorial/hard_code_factorial.py"
with open(file_root, "w") as file:
    file.write("get_factorial_of = input(\"Please give me a number to get the factorial of, pal.\\n> \")\n")
    file.write("get_factorial_of = int(get_factorial_of)\n")
    conditional_num = 1
    for key in factorial_answers:
        if conditional_num == 1:
            file.write("if get_factorial_of == {}:\n".format(key))
        else:
            file.write("elif get_factorial_of == {}:\n".format(key))
        file.write("\tprint({})\n".format(factorial_answers.get(key)))
        conditional_num += 1
    file.write("else:\n")
    file.write("\tprint(\"This number has not been hard coded in to this file, sorry bud.\")\n")
