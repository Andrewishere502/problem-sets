from random import randint


def rand_list(num, min_=1, max_=9):
    return [randint(min_, max_) for _ in range(num)]


def mean(list_):
    total = sum(list_)   
    mean = total / len(list_)
    return mean


def get_frequencies(list_):
    frequencies = {}
    for num in list_:
        if frequencies.get(num) == None:
            frequencies[num] = 0
        frequencies[num] += 1
    return frequencies


def mode(frequency):
    modes = []
    last_frequency = 0
    for num, freq in frequency.items():
        if freq > last_frequency:
            modes = [num]
            last_frequency = freq
        elif freq == last_frequency:
            modes.append(num)
    if len(modes) == 1:
        modes = modes[0]
    return modes


def median(list_):
    new_list = sorted(list_)
    middle = len(new_list) / 2
    if isinstance(middle, float):
        min_mid = int(middle)
        max_mid = int(middle) + 1
        med = set([new_list[i] for i in range(min_mid, max_mid+1)])
        if len(med) == 1:
            med = list(med)[0]  # convert to list cause set
                                # not subscriptable
    else:
        med = new_list[middle]
    return med


def frequency_plot(frequency):
    min_ = min(list(frequency))
    max_ = max(list(frequency))
    y_axis = [i for i in range(min_, max_+1)]
    
    num_rows = max(frequency.values())
    graph = []
    for i in range(num_rows):
        row = []
        for num in y_axis:
            if frequency.get(num, 0) >= num_rows - i:
                row.append("X")
            else:
                row.append(" ")
        graph.append(row)
    graph.append(list(map(lambda i: str(i), y_axis)))
    for r in graph:
        print("   ".join(r))
    return

# list_ = [2,3,3,2,3,2,3,9,7,3,4,8,1,2,8,7,6,5,8,9,1,2,3,2,1,4,3,2,1,4,5,4,1,6,9,6,1,4,2,3,5]
list_ = [1, 3, 3, 3, 3, 1, 10]
# list_ = rand_list(41)

print("the mean is: " + str(mean(list_)))
print("the mode is: " + str(mode(get_frequencies(list_))))
print("the median is: " + str(median(list_)))

frequency_plot(get_frequencies(list_))
