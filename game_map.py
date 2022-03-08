from __future__ import annotations

from typing import Tuple, Iterable, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from entity import Actor
import tile_types
import calculator

if TYPE_CHECKING:
    from entity import Entity, Camera
    from engine import Engine


class GameMap:
    def __init__(
        self, 
        engine: Engine,
        width: int, height: int,
        entities: Iterable[Entity] = (),
        fog: bool = True,
    ) -> None:
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        # To keep track of what the player should see.
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")
        self.fog = fog

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (
            entity 
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

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
    
    def pos_from_console_pos(self, pos: Tuple[int, int], console: Console, camera: Camera) -> Tuple[int, int]:
        zero = calculator.tuple_subtract(camera.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_add(pos, zero)

    def render(self, console: Console, camera: Camera) -> None:  # (x, y) is camera location
        # Calculate Bounds for drawing map.
        xm, ym = self.pos_from_console_pos((0, 0), console, camera)
        xm_1, ym_1 = max(0, xm), max(0, ym)
        xm_2, ym_2 = min(xm + console.width, self.width), min(ym + console.height, self.height)
        xc_1, yc_1 = max(0, -xm), max(0, -ym)
        xc_2, yc_2 = xc_1 + xm_2 - xm_1, yc_1 + ym_2 - ym_1
        if self.fog:
            console.rgb[xc_1:xc_2, yc_1:yc_2] = np.select(
                condlist=[self.visible[xm_1:xm_2, ym_1:ym_2], self.explored[xm_1:xm_2, ym_1:ym_2]],
                choicelist=[self.tiles["light"][xm_1:xm_2, ym_1:ym_2], self.tiles["dark"][xm_1:xm_2, ym_1:ym_2]],
                default=tile_types.SHROUD
            )
        else:
            console.rgb[xc_1:xc_2, yc_1:yc_2] = np.select(
                condlist=[self.visible[xm_1:xm_2, ym_1:ym_2], self.explored[xm_1:xm_2, ym_1:ym_2]],
                choicelist=[self.tiles["light"][xm_1:xm_2, ym_1:ym_2], self.tiles["dark"][xm_1:xm_2, ym_1:ym_2]],
                default=self.tiles["dark"][xm_1:xm_2, ym_1:ym_2]
            )

        entities_sorted_for_rendering = sorted(self.entities, key = lambda x: x.render_order.value)

        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV
            if self.visible[entity.pos]:
                console.print(
                    x=entity.x - camera.x + int(console.width/2), 
                    y=entity.y - camera.y + int(console.height/2), 
                    string=entity.char, fg=entity.color)
