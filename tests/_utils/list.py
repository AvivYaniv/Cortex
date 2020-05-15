
def is_interleaved_list(lst):
    last = lst[0]
    blocks = { last }
    for i in range(1, len(lst)):
        current = lst[i]
        # If in same block
        if current == last:
            continue
        # If new block id has occurred - therefore interleaving
        if current in blocks:
            return True
        # Add to blocks
        blocks.add(current)
        # Update last block to current
        last = current
    return False
