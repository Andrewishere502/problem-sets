import os


def clear_screen():
    os.system("clear")
    return


def get_total_min(start, end):
    start_date_time = start.split(" ") # splits date and time into list
    start_date = start_date_time[0].split("/") # gets date split day month and year into list
    start_time = start_date_time[1].split(":") # gets time split hours and minutes into list
    
    end_date_time = end.split(" ") # splits date and time into list
    end_date = end_date_time[0].split("/") # gets date split day month and year into list
    end_time = end_date_time[1].split(":") # gets time split hours and minutes into list

    # calculate the time difference between start and end dates
    num_years = int(end_date[2]) - int(start_date[2]) # remember that the items in the list are strings
    num_months = int(end_date[1]) - int(start_date[1])
    num_days = int(end_date[0]) - int(start_date[0])
    num_hours = int(end_time[0]) - int(start_time[0])
    num_min = int(end_time[1]) - int(start_time[1])

    total_time_in_min = (num_years*365*24*60) + (num_months*30*24*60) + (num_days*24*60) + (num_hours*60) + num_min

    return total_time_in_min


# start = input("What date and time did you arrive in the garage?\n(e.g. 19/3/1930 16:34)\n> ")
start = "18/3/1931 16:34"
# end_time = input("What date and time did you leave the garage?\n(e.g. 19/3/1930 16:34)\n> ")
end = "18/3/1930 16:34"
total_time_in_min = get_total_min(start, end)
print("You were parked for {} minutes in the garage.".format(total_time_in_min))

if total_time_in_min < 0:
    print("You can't spend negative time somewhere!")
elif total_time_in_min == 0:
    print("Why did you spend no time in the garage?")
else:
    if total_time_in_min <= 30:
        payment = 0.5
    elif total_time_in_min > 30 and total_time_in_min < 160:
        payment = 0.5 + 5
    elif total_time_in_min >= 160 and total_time_in_min <= 320:
        payment = 3
    elif total_time_in_min > 320 and total_time_in_min < 1440:
        payment = 3 + 15
    elif total_time_in_min > 1440 and total_time_in_min < 2880:
        payment = 30
    else:
        payment = 30 * total_time_in_min//2880
    print("You must pay {}".format(payment))