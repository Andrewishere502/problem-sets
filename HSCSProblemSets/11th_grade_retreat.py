import random


def calc_success(first_choice_num, second_choice_num, no_choice_num):
    # first_choice_num -- number of students who got their first choice
    # second_choice_num -- number of students who got their second choice
    # no_choice_num -- number of students who didn't get either choice
    total = first_choice_num + second_choice_num + no_choice_num
    first_choice_percent = "{:.2%}".format(first_choice_num / total)
    second_choice_percent = "{:.2%}".format(second_choice_num / total)
    no_choice_percent = "{:.2%}".format(no_choice_num / total)
    return first_choice_percent, second_choice_percent, no_choice_percent


TOTAL_STUDENTS = 80
student_choices = {key: random.sample(range(1, 11), 2) for key in range(TOTAL_STUDENTS)}

activities = {key: [] for key in range(1, 11)}

first_choice_num = 0
second_choice_num = 0
students_with_no_activity = []
for student, choices in student_choices.items():
    first, second = choices
    if len(activities[first]) < 8:
        activities[first].append(student)
        first_choice_num += 1
    elif len(activities[second]) < 8:
        activities[second].append(student)
        second_choice_num += 1
    else:
        students_with_no_activity.append(student)

print(activities)
print(students_with_no_activity)
print(calc_success(first_choice_num, second_choice_num, len(students_with_no_activity)))
