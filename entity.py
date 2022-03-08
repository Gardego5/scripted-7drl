from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

from tcod import Console

from render_order import RenderOrder
import calculator

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

from numpy import char

import calculator

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    game_map: GameMap

    def __init__(
        self,
        *,
        game_map: Optional[GameMap] = None,
        pos: Tuple[int, int] = (None, None), 
        char: str = "?", color: Tuple[int, int, int] = (None, None, None),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ) -> None:
        self.pos = pos
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)
    
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

    def spawn(self: T, pos: Tuple[int, int] = (None, None), game_map: Optional[GameMap] = None) -> T:
        clone = copy.deepcopy(self)
        if pos != None: clone.pos = pos
        if game_map != None: game_map.entities.add(clone)
        return clone

    # Places entity at new location. Handles moving across GameMaps.
    def place(self, pos: Tuple[int, int], game_map: Optional[GameMap] = None) -> None:
        self.pos = pos
        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)

    def move(self, delta: Tuple[int, int]) -> None:
        self.pos = calculator.tuple_add(self.pos, delta)

class Actor (Entity):
    def __init__(
        self,
        *,
        pos: Tuple[int, int] = (None, None),
        char: str = "?",
        color: Tuple[int, int, int] = (None, None, None),
        name: str = "<Unnamed>",
        blocks_movement: bool = True,
        ai_cls: Type[BaseAI],
        fighter: Fighter,
    ) -> None:
        super().__init__(
            pos = pos,
            char = char,
            color = color,
            name = name,
            blocks_movement = blocks_movement,
            render_order = RenderOrder.ACTOR
        )
        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)

class Camera (Entity):
    def __init__(self, pos: Tuple[int, int] = None, entity: Entity = None):
        super().__init__(pos=pos, char="&", color=(240, 210, 100), name="<Camera>")
        self.entity = entity

    @classmethod
    def from_entity(cls, entity: Entity) -> Camera:
        return Camera(entity.pos, entity)
    
    def follow(self, entity: Entity = None):
        if entity != None: self.entity = entity
        self.pos = self.entity.pos

    def console_to_game_map(self, console: Console, pos: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
        zero = calculator.tuple_subtract(self.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_add(pos, zero)
    
    def game_map_to_console(self, console: Console, pos: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
        offset = calculator.tuple_subtract(self.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_subtract(pos, offset)