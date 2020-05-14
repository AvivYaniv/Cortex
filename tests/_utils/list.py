
def is_interleaved_list(lst):
    last_item = lst[0]
    for i in range(1, 1+len(lst)):
        if lst[i] != last_item:
            return True
        last_item = lst[i]
    return False
