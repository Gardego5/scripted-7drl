from __future__ import annotations

from typing import Tuple, Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from entity import Actor, Item
import tile_types
import calculator

if TYPE_CHECKING:
    from entity import Entity, Camera
    from engine import Engine


class GameMap:
    down_stairs: optional[Tuple[int, int]] = None
    up_stairs: optional[Tuple[int, int]] = None

    def __init__(
        self, 
        engine: Engine,
        width: int, height: int,
        fog: bool = True,
    ) -> None:
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set()

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.clock = {}

        # To keep track of what the player should see.
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")
        self.fog = fog

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (entity for entity in self.entities if isinstance(entity, Actor) and entity.is_alive)
    
    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def add_to_clock(self, actor: Actor, time: Optional[float] = None) -> None:
        try:
            t = min(self.clock) + time if time is not None else actor.fighter.acting_time
        except ValueError:
            t = time if time is not None else actor.fighter.acting_time

        try:
            self.clock[t].append(actor)
        except KeyError:
            self.clock[t] = [actor]

    def get_blocking_entity_at_location(self, pos: Tuple[int, int]) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.pos == pos:
                return entity
        return None

    def get_actor_at_location(self, pos: Tuple[int, int]):
        for actor in self.actors:
            if actor.pos == pos:
                return actor
        return None

    def in_bounds(self, pos: Tuple[int, int]) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def render(self, console: Console, camera: Camera) -> None:  # (x, y) is camera location
        # Calculate Bounds for drawing map.
        xm, ym = camera.console_to_game_map(console = console)
        xm_1, ym_1 = max(0, xm), max(0, ym)
        xm_2, ym_2 = min(xm + console.width, self.width), min(ym + console.height, self.height)
        xc_1, yc_1 = max(0, -xm), max(0, -ym)
        xc_2, yc_2 = xc_1 + xm_2 - xm_1, yc_1 + ym_2 - ym_1
        if self.fog:
            console.rgb[xc_1:xc_2, yc_1:yc_2] = np.select(
                condlist=[self.explored[xm_1:xm_2, ym_1:ym_2]],
                choicelist=[self.tiles["graphic"][xm_1:xm_2, ym_1:ym_2]],
                default=tile_types.SHROUD
            )
            console.rgb["fg"] = console.rgb["fg"] // 1.4
            console.rgb["bg"] = console.rgb["bg"] // 1.4
            console.rgb[xc_1:xc_2, yc_1:yc_2] = np.select(
                condlist=[self.visible[xm_1:xm_2, ym_1:ym_2]],
                choicelist=[self.tiles["graphic"][xm_1:xm_2, ym_1:ym_2]],
                default=console.rgb[xc_1:xc_2, yc_1:yc_2]
            )
        else:
            console.rgb[xc_1:xc_2, yc_1:yc_2] = self.tiles["graphic"][xm_1:xm_2, ym_1:ym_2]
            console.rgb["fg"] = console.rgb["fg"] // 1.4
            console.rgb["bg"] = console.rgb["bg"] // 1.4
            console.rgb[xc_1:xc_2, yc_1:yc_2] = np.select(
                condlist=[self.visible[xm_1:xm_2, ym_1:ym_2]],
                choicelist=[self.tiles["graphic"][xm_1:xm_2, ym_1:ym_2]],
                default=console.rgb[xc_1:xc_2, yc_1:yc_2]
            )

        entities_sorted_for_rendering = sorted(self.entities, key = lambda x: x.render_order.value)

        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV
            if self.visible[entity.pos]:
                x, y = camera.game_map_to_console(entity.pos, console)
                console.print(x, y, string=entity.char, fg=entity.color)


class GameWorld:
    def __init__(
        self,
        engine: Engine,
        map_height: int, map_width: int,
        fog: bool = True,
    ) -> None:
        self.engine = engine

        self.map_width, self.map_height = map_width, map_height
        self.fog = fog

        self.game_maps = []
        self.current_floor_num = 0

    @property
    def current_floor(self):
        return self.game_maps[self.current_floor_num]

    def generate_floor(self) -> None:
        from procgen import generate_dungeon

        self.game_maps.append(generate_dungeon(self.map_width, self.map_height, self.engine, len(self.game_maps)))
        self.game_maps[-1].fog = self.fog
