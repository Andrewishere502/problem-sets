length = int(input())
array = [int(n) for n in input().split(" ")]

pos_diffs = []
for i in range(1, length):
    diff = array[i-1] - array[i]
    if diff > 0:
        # Be sure to increment the number at the index which
        # is smaller than the number at the previous index.
        array[i] += diff
        pos_diffs.append(diff)

print(sum(pos_diffs))