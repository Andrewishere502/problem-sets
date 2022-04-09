# [id, badges, challenges, videos, [[quiz, attempts],[quiz, attempts]]]

user = [1234, 3, 12, 13, [[1, 4],[2, 3]]]

total_points = 0

badge_points = user[1] * 300  # 300 points per badge
total_points += badge_points

challenge_points = user[2] * 100  # 100 points per challenge
total_points += challenge_points

video_points = user[3] * 50  # 50 points per video
total_points += video_points

for quiz in user[-1]:
    points_for_quiz = quiz[-1] * 10  # 10 points per attempt 
                                     # because trying is the important part
    total_points += points_for_quiz

user_id = user[0]
print("User {} has {} points.".format(user_id, total_points))