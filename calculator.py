from typing import Tuple, Any
import math
import random

def tuple_add(*tuples) -> Tuple[Any]:
    return tuple(map(sum, zip(*tuples)))

def tuple_subtract(t1, t2) -> Tuple[Any]:
    return tuple(map(sum, zip(t1, map(lambda x: -x, t2))))

def tuple_distance(t1, t2) -> float:
    return math.sqrt((t1[0] - t2[0]) ** 2 + (t1[1] - t2[1]) ** 2)

def random_direction() -> Tuple[int, int]:
    dirs = [
        (-1, -1), ( 0, -1), ( 1, -1),
        (-1,  0), ( 0,  0), ( 1,  0),
        (-1,  1), ( 0,  1), ( 1,  1),
    ]
    return random.choice(dirs)