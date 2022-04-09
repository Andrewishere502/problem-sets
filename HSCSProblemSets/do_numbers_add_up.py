def search_list(list_to_search, target_num):
    for num in list_to_search:
        if target_num-num in list_to_search:
            if (num == target_num-num and list_to_search.count(num) >= 2) or num != target_num:
                return target_num-num in list_to_search
    return False

l = [14, 13, 15, 11]
t = 24
print(search_list(l, t))