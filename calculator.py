from typing import Tuple, Any

def tuple_add(*tuples) -> Tuple[Any]:
    return tuple(map(sum, zip(*tuples)))

def tuple_subtract(t1, t2) -> Tuple[Any]:
    return tuple(map(sum, zip(t1, map(lambda x: -x, t2))))