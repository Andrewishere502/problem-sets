def is_beautiful(perm):
    for i in range(len(perm) - 1):
        if abs(perm[i] - perm[i + 1]) == 1:
            return False
    return True


n = int(input())
if n == 1:
    print(n)
else:
    nums = list(range(1, n+1))

    evens = list(filter(lambda n: n % 2 == 0, nums))
    odds = list(filter(lambda n: n % 2 == 1, nums))

    if abs(evens[-1] - odds[0]) == 1:
        print("NO SOLUTION")
    else:
        evens.extend(odds)
        print(" ".join([str(n) for n in evens]))
