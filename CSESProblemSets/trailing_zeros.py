def count_mul_fives(n):
    total = 0
    pow = 1
    while True:
        count = n // 5 ** pow
        if count == 0:
            break
        else:
            pow += 1
            total += count
    return total


n = int(input())
total = count_mul_fives(n)
print(total)
