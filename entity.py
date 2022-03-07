from typing import Tuple

from numpy import char

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

class Camera (Entity):
    def __init__(self, x: int = None, y: int = None, entity: Entity = None):
        self.x = x
        self.y = y
        self.entity = entity
        self.char = "&"
        self.color = (240, 210, 100)

    @classmethod
    def from_entity(cls, entity: Entity):
        return Camera(entity.x, entity.y, entity)
    
    def follow(self, entity: Entity = None):
        if entity != None: self.entity = entity
        self.x = self.entity.x
        self.y = self.entity.y