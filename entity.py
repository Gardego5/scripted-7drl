from __future__ import annotations

import copy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

from numpy import char

import calculator

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(
        self, 
        pos: Tuple[int, int] = (None, None), 
        char: str = "?", color: Tuple[int, int, int] = (None, None, None),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
    ) -> None:
        self.pos = pos
        self.char = char
        self.color = color
        self.blocks_movement = blocks_movement
    
    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self) -> Tuple[int, int]:
        return self._x, self._y
    
    @pos.setter
    def pos(self, new_pos) -> None:
        self._x, self._y = new_pos

    def spawn(self: T, pos, game_map: GameMap = None) -> T:
        clone = copy.deepcopy(self)
        clone.pos = pos
        if game_map != None: game_map.entities.add(clone)
        return clone

    def move(self, delta: Tuple[int, int]) -> None:
        self.pos = calculator.tuple_add(self.pos, delta)

class Camera (Entity):
    def __init__(self, pos: Tuple[int, int] = None, entity: Entity = None):
        super().__init__(pos, "&", (240, 210, 100), name="<Camera>")
        self.entity = entity

    @classmethod
    def from_entity(cls, entity: Entity):
        return Camera(entity.pos, entity)
    
    def follow(self, entity: Entity = None):
        if entity != None: self.entity = entity
        self.pos = self.entity.pos