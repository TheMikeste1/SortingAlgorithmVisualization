from datetime import datetime
from datetime import timedelta


def bubble_sort_stepped(iterable):
    compares = 0
    swaps = 0
    time = timedelta()

    pass_len = len(iterable) - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(pass_len):
            compares += 1
            swap_now = False
            start = datetime.now()
            if iterable[i] > iterable[i + 1]:
                iterable[i], iterable[i + 1] = iterable[i + 1], iterable[i]
                swapped = True
                swap_now = True
                swaps += 1
            time += datetime.now() - start
            yield iterable, i, i + 1, swap_now

    return iterable, compares, swaps, time


def selection_sort_stepped(iterable):
    compares = 0
    swaps = 0
    time = timedelta()

    for i in range(len(iterable)):
        lowest = iterable[i]
        loc = i
        for j in range(i + 1, len(iterable)):
            temp = loc
            compares += 1
            start = datetime.now()
            if iterable[j] < lowest:
                lowest = iterable[j]
                loc = j
            time += datetime.now() - start
            yield iterable, temp, j, False
        swaps += 1
        start = datetime.now()
        iterable[i], iterable[loc] = iterable[loc], iterable[i]
        time += datetime.now() - start
        yield iterable, loc, i, True

    return iterable, compares, swaps, time


def insertion_sort_stepped(iterable):
    compares = 0
    swaps = 0
    time = timedelta()

    for i in range(1, len(iterable)):
        ele = iterable[i]
        placement_pos = i - 1

        while True:
            compares += 1
            start = datetime.now()
            if placement_pos >= 0 and ele < iterable[placement_pos]:
                placement_pos -= 1
                time += datetime.now() - start
                yield iterable, i, placement_pos + 1, False
            else:
                break

        placement_pos += 1
        time += datetime.now() - start

        if i != placement_pos:
            # Sometimes the element is already in the correct spot. It's more costly
            # remove and reinsert it, so we ought to check
            swaps += 1

            start = datetime.now()
            iterable.pop(i)
            iterable.insert(placement_pos, ele)
            time += datetime.now() - start
            yield iterable, placement_pos, -1, True

    return iterable, compares, swaps, time


def merge_sort_stepped(iterable, start=0, end=-1):
    compares = 0
    swaps = 0
    time = timedelta()

    if end < 0:
        end = len(iterable)
    if end - start == 1:
        # If there's only one element, go back up a level
        return iterable, compares, swaps, time

    # Get the middle of the section we're sorting
    #   end - start is the distance
    #      divided by 2 is the middle
    #   start + middle gives us the position in the array we're working on
    middle = start + (end - start) // 2

    # Recursively sort each half
    gen = merge_sort_stepped(iterable, start=start, end=middle)
    while True:
        try:
            out = gen.__next__()
            yield out
        except StopIteration as out:
            iterable = out.value[0].copy()
            compares = out.value[1]
            swaps = out.value[2]
            time = out.value[3]
            break

    gen = merge_sort_stepped(iterable, start=middle, end=end)
    while True:
        try:
            yield gen.__next__()
        except StopIteration as out:
            iterable = out.value[0].copy()
            compares += out.value[1]
            swaps += out.value[2]
            time += out.value[3]
            break

    # Get the number of elements each half is working with
    left = (end - start) // 2
    right = end - start - left

    # Sort each half
    while left and right:  # Ints are evaluated as true if greater than 1
        swapped = False
        compares += 1
        start_time = datetime.now()

        # start is at the front of the left half,
        # middle at the front of the right
        if iterable[start] > iterable[middle]:
            iterable.insert(start, iterable.pop(middle))
            right -= 1
            middle += 1
            swapped = True
            swaps += 1
        else:
            # Left is already in place
            left -= 1
        start += 1

        time += datetime.now() - start_time
        yield iterable, start - 1, middle if not swapped else middle - 1, swapped

    # We don't need to worry about inserting the leftovers if left or right
    # are greater than 1. They'll already be in place.

    return iterable, compares, swaps, time


def quicksort_stepped(iterable, start=0, end=-1):
    compares = 0
    swaps = 0
    time = timedelta()

    if end < 0:
        end = len(iterable) - 1

    if end - start < 1:
        # If there's only one element, we don't need to do anything.
        return iterable, compares, swaps, time

    # Get pivot
    pivot = iterable[end]

    # Partition
    j = start
    i = j - 1

    while j < end + 1:
        compares += 1

        yield iterable, end, j, False
        start_time = datetime.now()
        if iterable[j] < pivot:
            i += 1
            # If the item is less than the pivot move it down to
            # position i
            iterable[j], iterable[i] = iterable[i], iterable[j]

            time += datetime.now() - start_time
            swaps += 1
            yield iterable, j, i, True
            start_time = datetime.now()
        j += 1
        time += datetime.now() - start_time

    # Place the end to its final location
    iterable[end], iterable[i + 1] = iterable[i + 1], iterable[end]
    swaps += 1
    yield iterable, end, i + 1, True

    # Recursively sort parts on the left and right side of the pivot
    gen = quicksort_stepped(iterable, start=start, end=i)
    while True:
        try:
            out = gen.__next__()
            yield out
        except StopIteration as out:
            iterable = out.value[0].copy()
            compares += out.value[1]
            swaps += out.value[2]
            time += out.value[3]
            break

    gen = quicksort_stepped(iterable, start=i + 2, end=end)
    while True:
        try:
            out = gen.__next__()
            yield out
        except StopIteration as out:
            iterable = out.value[0].copy()
            compares += out.value[1]
            swaps += out.value[2]
            time += out.value[3]
            break

    return iterable, compares, swaps, time


def window_sort_stepped(iterable):
    compares = 0
    swaps = 0
    time = timedelta()

    num_elements = len(iterable)
    window_size = 2
    while True:
        for window in range(0, num_elements, window_size):
            right_size = window_size // 2
            center = window + right_size

            if center + right_size >= num_elements:
                right_size = num_elements - center

            while window < center and right_size > 0:
                compares += 1
                swapped = False
                start = datetime.now()
                if iterable[window] > iterable[center]:
                    iterable.insert(window, iterable.pop(center))
                    center += 1
                    right_size -= 1
                    swaps += 1
                    swapped = True
                window += 1

                time += datetime.now() - start
                yield iterable, window - 1, center - 1 if swapped else center, swapped

        if window_size > num_elements: break
        window_size *= 2
    return iterable, compares, swaps, time


def heapify_stepped(iterable, pos, num_elements):
    compares = 0
    swaps = 0
    time = timedelta()

    start = datetime.now()
    largest = iterable[pos]
    largest_i = pos

    """
    The formula to get the indices of the children node of a binary tree is as follows:

    Left  = 2i + 1
    Right = 2i + 2 (or Left + 1)

    where i is the current node index.

    Visualized here:
    [0, 1, 2, 3, 4, 5, 6] ->    
             [0]
           /    \
        [1]       [2]
       /   \     /   \
     [3]   [4] [5]    [6]

    """
    left_i = 2 * pos + 1
    right_i = left_i + 1

    if left_i < num_elements:
        compares += 1
        yield iterable, left_i, largest_i, False
        if iterable[left_i] > largest:
            largest = iterable[left_i]
            largest_i = left_i
    else:
        # If left_i is greater than the number of elements, so is right_i, so we can just return.
        return iterable, compares, swaps, time

    if right_i < num_elements:
        compares += 1
        yield iterable, right_i, largest_i, False
        if iterable[right_i] > largest:
            largest_i = right_i

    if largest_i != pos:
        iterable[pos], iterable[largest_i] = iterable[largest_i], iterable[pos]

        time += datetime.now() - start
        swaps += 1
        yield iterable, pos, largest_i, True

        gen = heapify_stepped(iterable, largest_i, num_elements)
        while True:
            try:
                yield gen.__next__()
            except StopIteration as out:
                iterable = out.value[0].copy()
                compares += out.value[1]
                swaps += out.value[2]
                time += out.value[3]
                break

    return iterable, compares, swaps, time


def heapsort_stepped(iterable):
    compares = 0
    swaps = 0
    time = timedelta()

    num_elements = len(iterable)

    # We need to build the initial max heap.
    # We can do this by going to the second to last level of the tree (the
    # last level has no children) and building the tree from the bottom up.
    #
    # A property of a binary tree is the (complete) layer below has the same
    # number of nodes as the sum of the layers above + 1. Therefore, we can
    # divide the number of elements and subtract 1 to get the last node of
    # the second to last layer.
    # Fortunately, this property gives us the last node with children when
    # the binary tree is not complete.
    for i in range(num_elements // 2 - 1, -1, -1):
        gen = heapify_stepped(iterable, i, num_elements)
        while True:
            try:
                yield gen.__next__()
            except StopIteration as out:
                iterable = out.value[0].copy()
                compares += out.value[1]
                swaps += out.value[2]
                time += out.value[3]
                break


    # Now that we've made our max heap, we can take the root element and
    # put it in the partitioned portion.
    num_elements -= 1
    # Continue the process while there are elements remaining
    while num_elements:
        iterable[0], iterable[num_elements] = iterable[num_elements], iterable[0]

        swaps += 1
        yield iterable, 0, num_elements, True

        gen = heapify_stepped(iterable, 0, num_elements)
        while True:
            try:
                yield gen.__next__()
            except StopIteration as out:
                iterable = out.value[0].copy()
                compares += out.value[1]
                swaps += out.value[2]
                time += out.value[3]
                break
        num_elements -= 1

    return iterable, compares, swaps, time
