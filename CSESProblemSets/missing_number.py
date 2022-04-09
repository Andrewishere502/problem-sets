def areth_sum(n):
    return int(n / 2 * (1 + n))

n = int(input())
nums = [int(n) for n in input().split(" ")]
missing_n = areth_sum(n) - sum(nums)
print(missing_n)