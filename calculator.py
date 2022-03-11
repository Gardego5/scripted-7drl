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

def lucky_chance(chance: int, luck: int, luckability: int = 3):
    # Calculates luck ajusted chance for you to succeed at something.
    # Luck improves your chance, while high luckability dampens the effect
    # of luck. Luckability represents the maximum fraction of the chance to
    # fail that can be removed. The higher the luckability, the more high
    # luck can have a beneficial impact, while the less of an impact a small
    # amount of luck has. 
    return chance/luckability*(luckability - 1) + (chance ** (luck/luckability + 1)) / luckability