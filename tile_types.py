from argparse import Namespace
from typing import Tuple

import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),
        ("transparent", np.bool),
        ("graphic", graphic_dt),
    ]
)

def new_tile(
    walkable: int,
    transparent: int,
    graphic: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, graphic), dtype=tile_dt)

# Plain graphics
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# Tiles
floor = new_tile(True, True, (ord(" "), (255, 255, 255), (180, 180, 210)))
wall = new_tile(False, False, (ord(" "), (255, 255, 255), (80, 80, 120)))
down_stairs = new_tile(True, True, (ord(">"), (255, 255, 255), (200, 180, 50)))
up_stairs = new_tile(True, True, (ord("<"), (255, 255, 255), (200, 180, 50)))

reserved = [
    down_stairs,
    up_stairs,
]
