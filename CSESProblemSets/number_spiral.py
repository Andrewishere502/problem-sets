# 2, 3 = 8
# 1, 1 = 1
# 4, 2 = 15

y, x = [int(n) for n in input().split(' ')]

if y == x:
    total = 1
    for i in range(x):
        total += i * 2

print(total)
