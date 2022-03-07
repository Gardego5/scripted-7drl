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
        ("dark", graphic_dt),
        ("light", graphic_dt),
    ]
)

def new_tile(
    *, # Enforce use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# Plain graphics
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# Tiles
floor = new_tile(
    walkable=True, transparent=True, 
    dark=(ord(" "), (255, 255, 255), (90, 90, 90)),
    light=(ord(" "), (255, 255, 255), (180, 180, 210)),
)
wall = new_tile(
    walkable=False, transparent=False, 
    dark=(ord(" "), (255, 255, 255), (60, 60, 60)),
    light=(ord(" "), (255, 255, 255), (80, 80, 120)),
)
