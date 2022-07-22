def bit_mask_to_list(bitmask: int, n: int) -> list:
    '''Return bitmask of length n converted to list of integers.'''
    return [i for i in range(1, n + 1) if bitmask & (1 << i)]