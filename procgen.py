from __future__ import annotations

from typing import Tuple, Callable, Iterator, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

import tcod

from game_map import GameMap
import generated_structures


def generate_dungeon(
    map_width: int, map_height: int,
    player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height, entities=[player])
    
    features = [
        generated_structures.Tower(10, 10, 60, 60),
    ]

    for feature in features:
        dungeon.tiles[feature.bounds] = feature.tiles

    return dungeon
