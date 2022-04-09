import random


class Die:
    def __init__(self):
        self.sides = 6
        self.images = {
            1: "# # # # # # # #\n#             #\n#             #\n#      .      #\n#             #\n#             #\n# # # # # # # #",
            2: "# # # # # # # #\n#             #\n#         .   #\n#             #\n#   .         #\n#             #\n# # # # # # # #",
            3: "# # # # # # # #\n#             #\n#         .   #\n#      .      #\n#   .         #\n#             #\n# # # # # # # #",
            4: "# # # # # # # #\n#             #\n#   .     .   #\n#             #\n#   .     .   #\n#             #\n# # # # # # # #",
            5: "# # # # # # # #\n#             #\n#   .     .   #\n#      .      #\n#   .     .   #\n#             #\n# # # # # # # #",
            6: "# # # # # # # #\n#             #\n#   .     .   #\n#   .     .   #\n#   .     .   #\n#             #\n# # # # # # # #"
            }
        return

    def roll(self):
        roll_val = random.randint(1, self.sides)
        return self.images[roll_val]


d = Die()
print(d.roll())