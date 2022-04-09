while True:
    user_input = input("Please input a sentence :)\n> ")

    word_list = user_input.split(" ")
    current_lowest_length = None
    current_lowest_word = None
    for word in word_list:
        try:
            if len(word) < current_lowest_length:
                current_lowest_length = len(word)
                current_lowest_word = word
        except TypeError:
            current_lowest_length = len(word)
            current_lowest_word = word

    print("{} is the shortest word of {} characters".format(current_lowest_word, current_lowest_length))
