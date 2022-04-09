n = int(input())
output = []
while n != 1:
    output.append(n)
    if n % 2 == 0:
        n = n // 2
    else:
        n = n * 3 + 1
print(" ".join([str(n) for n in output]) + " 1")