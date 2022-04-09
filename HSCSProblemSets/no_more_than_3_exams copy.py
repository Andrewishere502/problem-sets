import random


def make_assessment_cal(subjects, req_days=2):
    assessments = {
        "M": [],
        "T": [],
        "W": [],
        "TH": [],
        "F": []
        }
    for _ in range(req_days):
        exam_num = random.randint(2, 3)
        assessments[random.choice(list(assessments))] = (random.sample(subjects, exam_num))
    return assessments


def find_intersection(enrollment, subjects):
    intersections = set([])
    for subject in subjects:
        if len(intersections) == 0:
            intersections = enrollment[subject]
        else:
            intersections = intersections.intersection(enrollment[subject])
    return intersections


subjects = ["math", "science", "english", "spanish"]

# students = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
students = ["larry", "todd", "mark", "edmund", "sophia", "lily", "laura", "tootsie"]

enrollment = {subject: set(random.sample(students, 3)) for subject in subjects}
assessment_cal = make_assessment_cal(subjects)


message = "Warning, one or more students will have more than two exams on {} for classes {}. Please notify: {}"
for day, subjects in assessment_cal.items():
    if len(subjects) > 2:
        warning_students = find_intersection(enrollment, subjects)
        if len(warning_students) > 0:
            print(message.format(day, ", ".join(subjects), ", ".join(warning_students)))
