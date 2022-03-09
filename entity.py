from __future__ import annotations

import copy
from typing import Union, Optional, Tuple, TypeVar, TYPE_CHECKING

from tcod import Console

from render_order import RenderOrder
import calculator

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from components.consumable import Consumable
    from components.inventory import Inventory
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

from numpy import char

import calculator


class Entity:
    parent: Union[GameMap, Inventory]
    # A generic object to represent players, enemies, items, etc.
    def __init__(
        self,
        *,
        parent: Optional[Union[GameMap, Inventory]] = None,
        pos: Tuple[int, int] = (0, 0), 
        char: str = "?", color: Tuple[int, int, int] = (0, 0, 0),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
        inventory: Optional[Inventory] = None,
    ) -> None:
        self.pos = pos
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent: self.parent = parent
        if inventory: self.inventory = inventory
    
    @property
    def x(self) -> int:
        return self._x
    @x.setter
    def d(self, x: int) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y
    @y.setter
    def y(self, y: int) -> None:
        self._y = y

    @property
    def pos(self) -> Tuple[int, int]:
        return self._x, self._y
    @pos.setter
    def pos(self, new_pos) -> None:
        self._x, self._y = new_pos

    @property
    def game_map(self) -> GameMap:
        if hasattr(self, "parent"):
            if hasattr(self.parent, "entities"):
                return self.parent
    @game_map.setter
    def game_map(self, game_map: GameMap) -> None:
        if hasattr(self, "parent"):
            if hasattr(self.parent, "entities"):
                self.parent.entities.remove(self)
            elif hasattr(self.parent, "items"):
                self.parent.items.remove(self)
        self.parent = game_map
        self.parent.entities.add(self)

    @property
    def container(self) -> Inventory:
        if hasattr(self, "parent"):
            if hasattr(self.parent, "items"):
                return self.parent
    @container.setter
    def container(self, container: Inventory):
        if hasattr(self, "parent"):
            if hasattr(self.parent, "entities"):
                self.parent.entities.remove(self)
            elif hasattr(self.parent, "items"):
                self.parent.items.remove(self)
        self.parent = container
        self.parent.items.append(self)

    @property
    def inventory(self) -> Inventory:
        return self._inventory
    @inventory.setter
    def inventory(self, inventory: Inventory) -> None:
        if hasattr(self, "_inventory"):
            del self._inventory.entity
        self._inventory = inventory
        self._inventory.entity = self

    def spawn(self: T, pos: Tuple[int, int] = (0, 0), game_map: Optional[GameMap] = None) -> T:
        # Spawns a new copy of the entity at the given position in the given GameMap.
        clone = copy.deepcopy(self)
        if pos != None: clone.pos = pos
        if game_map != None: clone.game_map = game_map
        return clone

    def place(self, pos: Tuple[int, int], game_map: Optional[GameMap] = None) -> None:
        # Places entity at new location. Handles moving across GameMaps.
        self.pos = pos
        if game_map:
            self.game_map = game_map

    def move(self, delta: Tuple[int, int]) -> None:
        self.pos = calculator.tuple_add(self.pos, delta)


class Actor (Entity):
    def __init__(
        self,
        *,
        parent: Optional[Union[GameMap, Inventory]] = None,
        pos: Tuple[int, int] = (0, 0),
        char: str = "?",
        color: Tuple[int, int, int] = (0, 0, 0),
        name: str = "<Unnamed>",
        blocks_movement: bool = True,
        ai_cls: Type[BaseAI],
        fighter: Fighter,
        inventory: Optional[Inventory] = None,
    ) -> None:
        super().__init__(
            parent = parent,
            pos = pos,
            char = char,
            color = color,
            name = name,
            blocks_movement = blocks_movement,
            render_order = RenderOrder.ACTOR,
            inventory = inventory,
        )
        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter

    @property
    def fighter(self) -> Fighter:
        return self._fighter
    @fighter.setter
    def fighter(self, fighter: Fighter):
        if hasattr(self, "_fighter"):
            del self._fighter.entity
        self._fighter = fighter
        self._fighter.entity = self

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)


class Item (Entity):
    def __init__(
        self,
        *,
        parent: Optional[Union[GameMap, Inventory]] = None,
        pos: Tuple[int, int] = (0, 0),
        char: str = "?",
        color: Tuple[int, int, int] = (0, 0, 0),
        name: str = "<Unnamed>",
        consumable: Consumable = None,
        inventory: Optional[Inventory] = None,
    ) -> None:
        super().__init__(
            parent = parent,
            pos = pos,
            char = char,
            color = color,
            name = name,
            blocks_movement = False,
            render_order = RenderOrder.ITEM,
            inventory = inventory,
        )

        if consumable: self.consumable = consumable
    
    @property
    def consumable(self) -> Consumable:
        return self._consumable
    @consumable.setter
    def consumable(self, consumable) -> None:
        if hasattr(self, "_consumable"):
            del self._consumable.entity
        self._consumable = consumable
        self._consumable.entity = self


class Camera (Entity):
    # A helper Entity, not usually rendered, used for math to center the
    # game map on the console.
    def __init__(self, pos: Tuple[int, int] = None, entity: Entity = None):
        super().__init__(pos=pos, char="&", color=(240, 100, 100), name="<Camera>")
        self.entity = entity

    @classmethod
    def from_entity(cls, entity: Entity) -> Camera:
        return Camera(entity.pos, entity)
    
    def follow(self, entity: Entity = None) -> None:
        # Sets the Camera to follow a new Entity if provided, 
        # and then updates the Camera's location to the location of the followed Entity.
        if entity != None: self.entity = entity
        if not hasattr(self, "entity"): raise AttributeError("Camera is not following any Entity.")
        self.pos = self.entity.pos

    def console_to_game_map(self, console: Console, pos: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
        # Takes a position relative to the console and returns it's position on the gamemap.
        zero = calculator.tuple_subtract(self.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_add(pos, zero)
    
    def game_map_to_console(self, console: Console, pos: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
        # Takes a position relative to the game map and returns it's position on the console.
        offset = calculator.tuple_subtract(self.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_subtract(pos, offset)

    def render(self, console: Console) -> None:
        # Draws a visual representation of the Camera on the console.
        x, y = self.game_map_to_console(console, self.pos)
        console.print(x + 1, y - 1, "L", fg = self.color)
        console.print(x + 2, y - 2, self.char, fg = self.color)