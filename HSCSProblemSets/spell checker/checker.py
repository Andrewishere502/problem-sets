import re
import datetime


class SpellChecker:
    def __init__(self, file_path):
        file_lines = open(file_path, "r").readlines()
        self.valid_words = set([line[:-1] for line in file_lines])  # remove \n
        return

    @staticmethod
    def get_unique_words(book_path):
        file_lines = open(book_path, "r").readlines()
        book_lines = [line for line in file_lines]  # remove \n
        book_words = set([])
        for line in book_lines:
            words = line.split()
            for word in words:
                word = word.lower()
                invalid_character = re.findall(r"[^a-zA-z]", word)
                for char in invalid_character:
                    word = word.replace(char, "")
                if word != "":
                    book_words.add(word)
        return book_words

    def get_invalid_words(self, book_path):
        start_time = datetime.datetime.now()
        book_words = self.get_unique_words(book_path)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Word parsing took {}μs".format(elapsed_time.microseconds))

        start_time = datetime.datetime.now()
        invalid_words = [word for word in book_words if word not in self.valid_words]
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Book correction took {}μs".format(elapsed_time.microseconds))
        return invalid_words


checker = SpellChecker("spell_checker/valid_words.txt")
checker.get_invalid_words("spell_checker/KingJames.txt")
