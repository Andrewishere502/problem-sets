import random


teams = [
    "Pablo",
    "Andrew",
    "Yoyo",
    "Tony",
    "Niki",
    "Anya",
    "Leo",
    "Sophi"
    ]

matches = []
for i in range(len(teams) // 2):  # create max num matches
    match = random.sample(teams, 2)
    matches.append(match)
    for m in match:  # remove matches from being selected again
        teams.remove(m)

for match in matches:
    print(match[0], "+", match[1])

if len(teams) > 0:
    print("!" * 20)
    print("These people didn't get a match:")
    for team in teams:
        print(team)