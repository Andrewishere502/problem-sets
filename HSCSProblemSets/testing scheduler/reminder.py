import pathlib
import os
import datetime
import time


def parse_file(filename):
    PATH = pathlib.Path(os.getcwd())
    schedule = []
    with open(PATH / filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.split("\t")
            time = line[0]
            people = line[1:]
            # make sure people are scheduled for this time
            if people[0] != '' and people[1] != "\n":
                schedule.append((time, people[0], people[1][:-1]))  # remove \n
    return schedule


def flash_current_time_slot(i):
    formdic = dict(zip(["time", "person1", "person2"], schedule[i]))
    print("checking {person1} and {person2} at {time}".format(**formdic))
    return


filename = "testing_schedule.txt"
schedule = parse_file(filename)

i = 0
flash_current_time_slot(i)
while i < len(schedule):
    scheduled_time = schedule[i][0]
    hour, minute = [int(i) for i in scheduled_time.split(":")]  # hour and min are ints
    now = datetime.datetime.now()
    # now = datetime.time(hour=8, minute=42)
    if hour < now.hour or minute < now.minute:
        i += 1
    if hour == now.hour and minute <= now.minute + 3:  # remind 3 minutes early
        os.system("say %s and %s have testing in 3 minutes." % schedule[i][1:])
        i += 1  # increment to the next time in the schedule
        flash_current_time_slot(i)
    time.sleep(60)  # wait a minute