from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity, Camera


class GameMap:
    def __init__(
        self, 
        width: int, height: int,
        entities: Iterable[Entity] = (),
    ) -> None:
        self.width, self.height = width, height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")
    
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console, camera: Camera) -> None:  # (x, y) is camera location
        # Calculate Bounds for drawing map.
        xm, ym = camera.x - int(console.width / 2), camera.y - int(console.height / 2)
        xm_1, ym_1 = max(0, xm), max(0, ym)
        xm_2, ym_2 = min(xm + console.width, self.width), min(ym + console.height, self.height)
        xc_1, yc_1 = max(0, -xm), max(0, -ym)
        xc_2, yc_2 = xc_1 + xm_2 - xm_1, yc_1 + ym_2 - ym_1
        console.rgb[xc_1:xc_2, yc_1:yc_2] = np.select(
            condlist=[self.visible[xm_1:xm_2, ym_1:ym_2], self.explored[xm_1:xm_2, ym_1:ym_2]],
            choicelist=[self.tiles["light"][xm_1:xm_2, ym_1:ym_2], self.tiles["dark"][xm_1:xm_2, ym_1:ym_2]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x - camera.x + int(console.width/2), 
                    y=entity.y - camera.y + int(console.height/2), 
                    string=entity.char, fg=entity.color)
