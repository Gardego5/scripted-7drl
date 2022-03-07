from typing import Tuple, Any

def tuple_add(*tuples) -> Tuple[Any]:
    return tuple(map(sum, zip(*tuples)))