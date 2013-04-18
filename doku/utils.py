import math
import re


def box_size(size):
    result = math.sqrt(size)
    box_size = int(result)

    if box_size != result:
        msg = 'Size is not a perfect square. Cannot find a box size.'
        raise ValueError(msg)

    return box_size


def isplit(s, sep=None):
    pattern = re.compile(r'\s+' if sep is None else re.escape(sep))
    length = len(s)
    pos = 0

    while True:
        match = pattern.search(s, pos)

        if not match:
            if pos < length or sep is not None:
                yield s[pos:]
            break

        if pos < match.start() or sep is not None:
            yield s[pos:match.start()]

        pos = match.end()
