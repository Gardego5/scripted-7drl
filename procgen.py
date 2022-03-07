from __future__ import annotations

from typing import Tuple, Callable, Iterator, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

import random

import tcod

from game_map import GameMap
import generated_structures


def place_entities(
    room: Room,
    dungeon: GameMap,
    max_monsters: int = None,
    min_monsters: int = 0,
) -> None:
    if max_monsters == None: max_monsters = int(room.area/10)
    number_of_monsters = random.randint(min_monsters, max_monsters)

    for i in range(number_of_monsters):
        while i < room.area:  # Choose location for new entity
            x = random.randint(room.x1, room.x2)
            y = random.randint(room.y1, room.y2)
            # Increment counter if entity already at chosen site to prevent infinite loop.
            if any(entity.x == x and entity.y == y for entity in dungeon.entities): i += 1
            # If no entity already at chosen site and site is walkable, break loop and use chosen site
            elif dungeon.tiles[x, y]["walkable"]: break

        # TODO place entities at chosen site.
        


def generate_dungeon(
    map_width: int, map_height: int,
    player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height, entities=[player])
    
    structures = [
        generated_structures.Tower(10, 10, 60, 60),
    ]

    simple_structures = []

    for structure in structures:
        dungeon.tiles[structure.bounds] = structure.tiles
        if structure.features:
            simple_structures.extend(structure.features)

    for structure in simple_structures:
        place_entities(structure, dungeon)

    return dungeon
