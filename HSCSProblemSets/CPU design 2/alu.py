def ALU(num1, num2, sub=False):
    """Return the sum/difference between two number."""
    sum_ = num1 + num2 * (-1 if sub else 1)
    return sum_


if __name__ == "__main__":
    print(ALU(2, -7))