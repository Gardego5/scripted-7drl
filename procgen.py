from __future__ import annotations

from typing import Tuple, Callable, Iterator, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

import random

import tcod

from game_map import GameMap
import generated_structures
import entity_factories


def place_an_entity_randomly(
    room: Room,
    dungeon: GameMap,
    entity: Entity,
) -> None:
    i = 0
    while i < room.area:  # Choose location for new entity
        pos = random.randint(room.x1, room.x2), random.randint(room.y1, room.y2)
        # Increment counter if entity already at chosen site to prevent infinite loop.
        if any(entity.pos == pos for entity in dungeon.entities): i += 1
        # If no entity already at chosen site and site is walkable, break loop and use chosen site
        elif dungeon.tiles[pos]["walkable"]: break

    entity.place(pos, dungeon)

def place_entities(
    room: Room,
    dungeon: GameMap,
    max_monsters: int = None,
    min_monsters: int = 0,
    max_items: int = None,
    min_items: int = 0,
) -> None:
    if max_monsters == None: max_monsters = int(room.area/10)
    number_of_monsters = random.randint(min_monsters, max_monsters)
    if max_items == None: max_items = int(room.area/25)
    number_of_items = random.randint(min_items, max_items)

    for i in range(number_of_monsters):
        chosen_monster = random.choices(list(entity_factories.enemies.values()), list(entity_factories.enemies.keys()))[0].spawn()
        place_an_entity_randomly(room, dungeon, chosen_monster)
    for i in range(number_of_items):
        chosen_item = random.choices(list(entity_factories.items.values()), list(entity_factories.items.keys()))[0].spawn()
        place_an_entity_randomly(room, dungeon, chosen_item)

# TODO: Parameterize generate dungeon. 
def generate_dungeon(
    map_width: int, map_height: int,
    engine: engine,
) -> GameMap:
    player = engine.player

    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    
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

    place_an_entity_randomly(random.choice(simple_structures), dungeon, player)

    return dungeon
