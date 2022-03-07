from typing import Tuple

from numpy import char

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, pos: Tuple[int, int], char: str, color: Tuple[int, int, int]) -> None:
        self.pos = pos
        self.char = char
        self.color = color
    
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

    def move(self, dx: int, dy: int) -> None:
        self._x += dx
        self._y += dy

class Camera (Entity):
    def __init__(self, pos: Tuple[int, int], entity: Entity = None):
        super().__init__(pos, "&", (240, 210, 100))
        self.entity = entity

    @classmethod
    def from_entity(cls, entity: Entity):
        return Camera(entity.pos, entity)
    
    def follow(self, entity: Entity = None):
        if entity != None: self.entity = entity
        self.pos = self.entity.pos