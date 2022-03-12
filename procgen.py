from __future__ import annotations

from typing import Tuple, Callable, Iterator, Iterable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

import random

import tcod

from game_map import GameMap
import generated_structures
import entity_factories
import exceptions
import calculator
import tile_types


def random_suitable_pos(
    room: Room,
    dungeon: GameMap,
    criteria: Optional[Callable[[Tuple[int, int], int], bool]] = None,
    tenacity: float = 1.0,
) -> Tuple[int, int]:
    if not criteria:
        criteria = lambda pos, attempt: not any(entity.pos == pos for entity in dungeon.entities) and dungeon.tiles[pos]["walkable"] and dungeon.tiles[pos] not in tile_types.reserved

    i = 0
    while i < room.area * tenacity:
        pos = random.randint(room.x1, room.x2), random.randint(room.y1, room.y2)
        if criteria(pos, i):
            return pos
        i += 1
    
    raise exceptions.GenerationException(f"Took too long to find a suitable position in {room}, giving up.")

def place_an_entity_randomly(
    room: Room,
    dungeon: GameMap,
    entity: Entity,
) -> None:
    try:
        pos = random_suitable_pos(room, dungeon)
        entity.place(pos, dungeon)
    except exceptions.GenerationException:
        pass

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

def place_stairs(
    rooms: Iterable[Room],
    dungeon: GameMap,
    up: bool = False,
) -> Tuple[int, int]:
    def suitable(pos: Tuple[int, int], attempt: int) -> bool:
        # Preferably use a corner, unless it takes too long, and then 
        # give up and use any point out in the open that fits the other 
        # requirements.
        if attempt < 100:
            neighbors = [dungeon.tiles[calculator.tuple_add(delta, pos)] == tile_types.wall for delta in calculator.adjacent]

            return (not any(entity.pos == pos for entity in dungeon.entities)
                    and dungeon.tiles[pos]["walkable"]
                    and dungeon.tiles[pos] not in tile_types.reserved
                    # Choose a tile that is in a corner.
                    and ((neighbors[0] and neighbors[1] and neighbors[3])
                        or (neighbors[1] and neighbors[2] and neighbors[4])
                        or (neighbors[3] and neighbors[5] and neighbors[6])
                        or (neighbors[4] and neighbors[6] and neighbors[7])))
        else:
            return (not any(entity.pos == pos for entity in dungeon.entities)
                    and dungeon.tiles[pos]["walkable"]
                    and dungeon.tiles[pos] not in tile_types.reserved)

    # Try to place stairs in a smaller room first.
    for room in sorted(rooms, key=lambda room: room.area * (random.random() + 1)):
        try:
            pos = random_suitable_pos(room, dungeon, suitable)

            if up:
                dungeon.tiles[pos] = tile_types.up_stairs
                dungeon.up_stairs = pos
            else:
                dungeon.tiles[pos] = tile_types.down_stairs
                dungeon.down_stairs = pos

            return pos
        except exceptions.GenerationException:
            pass
    raise exceptions.GenerationException("Generation Failed: Couldn't find a suitable place for the stairs.")

# TODO: Parameterize generate dungeon. 
def generate_dungeon(
    map_width: int, map_height: int,
    engine: engine,
) -> GameMap:
    player = engine.player

    dungeon = GameMap(engine, map_width, map_height)
    
    structures = [
        generated_structures.Tower(10, 10, 60, 60),
    ]

    simple_structures = []

    for structure in structures:
        dungeon.tiles[structure.bounds] = structure.tiles
        if hasattr(structure, "features"):
            simple_structures.extend(structure.features)
        else:
            simple_structures.append(structure)

    place_stairs(simple_structures, dungeon)

    for structure in simple_structures:
        place_entities(structure, dungeon)

    place_an_entity_randomly(random.choice(simple_structures), dungeon, player)

    return dungeon
