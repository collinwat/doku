import math


def box_size(size):
    result = math.sqrt(size)
    box_size = int(result)

    if box_size != result:
        msg = 'Size is not a perfect square. Cannot find a box size.'
        raise ValueError(msg)

    return box_size
