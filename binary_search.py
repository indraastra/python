NOT_FOUND = -1

def middle_index(low, high):
    return low + ((high - low) / 2)


def __binary_search__(T, A, low, high):
    mid = middle_index(low, high)
    val = A[mid]
    if val == T:
        return mid
    elif T > val and mid != low:
        return __binary_search__(T, A, mid, high)
    elif T < val and mid != high:
        return __binary_search__(T, A, low, mid)
    else:
        return NOT_FOUND


def binary_search(T, A):
    # make sure array is sorted
    assert(sorted(A) == A)
    # if target isn't possibly within range, return immediately
    if len(A) == 0 or T < A[0] or T > A[-1]:
        return NOT_FOUND
    return __binary_search__(T, A, 0, len(A) - 1)


def test():
    assert(middle_index(0,  3) == 1)
    assert(middle_index(2,  3) == 2)
    assert(middle_index(3,  9) == 6)
    assert(middle_index(3, 10) == 6)

    assert(binary_search(3, [3]) == 0)
    assert(__binary_search__(4, [3], 0, 0) == NOT_FOUND)
    assert(__binary_search__(2, [3], 0, 0) == NOT_FOUND)
    assert(binary_search(100, [1, 2, 100, 1000]) == 2)
    assert(binary_search(100, [-1, 2, 5, 100,1000]) == 3)
    assert(binary_search(0, list(range(1000000))) == 0)
    assert(binary_search(100000, list(range(50000))) == NOT_FOUND)
    assert(binary_search(34567, list(range(0, 50000, 2))) == NOT_FOUND)

    print "all tests passed"

if __name__ == "__main__":
    test()
