def determine_exact_combo(flight_length):
    output = False
    for i in range(len(movie_lengths)):
        for movie in movie_lengths:
            if (movie_lengths[i] + movie == flight_length) and (movie_lengths[i] != movie):
                # first_movie = movie_lengths[i]
                # print(first_movie)
                # second_movie = movie
                # print(second_movie)
                # print("---")
                output = True
    return

movie_lengths = [110,150,159,180,100,145,185,90,93,98,102,122,120] # lengths of movies in minutes

while True:
    flight_length = input("How long is your flight in minutes?\n> ")
    try:
        flight_length = int(flight_length)
    except ValueError:
        print("ERROR invalid number please only type a number. i.e. '2'")
        continue
    print(determine_exact_combo(flight_length))