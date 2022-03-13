from __future__ import annotations

import copy
from typing import Union, Optional, Tuple, TypeVar, TYPE_CHECKING

from tcod import Console

from render_order import RenderOrder
from components.ai import HostileEnemy
from components.inventory import Inventory
import calculator

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from components.consumable import Consumable
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

from numpy import char

import calculator


class Entity:
    parent: Union[GameMap, Inventory]
    description: str = ""
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
    def ancestor(self) -> GameMap:
        if hasattr(self.parent, "entities"):
            return self.parent
        else:
            return self.parent.entity.ancestor

    @property
    def belongs_to_player(self) -> bool:
        if hasattr(self.parent, "entities"):
            if self is self.parent.player:
                return True
            else:
                return False
        else:
            return self.parent.entity.belongs_to_player

    @property
    def game_map(self) -> GameMap:
        if hasattr(self, "parent"):
            if hasattr(self.parent, "entities"):
                return self.parent
    @game_map.setter
    def game_map(self, game_map: GameMap) -> None:
        if hasattr(self, "parent"):
            if hasattr(self.parent, "entities"):
                print("hi1")
                if hasattr(self, "hardware"): print(len(self.game_map.entities))
                self.parent.entities.remove(self)
                if hasattr(self, "hardware"): print(len(self.game_map.entities))
            elif hasattr(self.parent, "items"):
                print("hi2")
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
        else:
            self.game_map = self.ancestor

    def distance(self, pos) -> float:
        return calculator.tuple_distance(pos, self.pos)

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


class Player (Actor):
    def __init__(
        self,
        *,
        parent: Optional[Union[GameMap, Inventory]] = None,
        pos: Tuple[int, int] = (0, 0),
        fighter: Fighter,
        inventory: Optional[Inventory] = None,
    ) -> None:
        super().__init__(
            parent = parent,
            pos = pos,
            char = "#",
            color = (255, 255, 255),
            name = "Player",
            blocks_movement = True,
            ai_cls = HostileEnemy,
            inventory = inventory,
            fighter = fighter,
        )
        
        self.hardware = Inventory(16)
        self.software = Inventory(3)


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

        if consumable:
            self.consumable = consumable
            self.consumable.entity = self
    
    @property
    def consumable(self) -> Consumable:
        return self._consumable
    @consumable.setter
    def consumable(self, consumable) -> None:
        self._consumable = consumable
        self._consumable.entity = self


class Camera (Entity):
    # A helper Entity, not usually rendered, used for math to center the
    # game map on the console. Keeps track of its current console and updates
    # its console whenever it is passed a new one.
    def __init__(self, pos: Tuple[int, int] = None, entity: Optional[Entity] = None, console: Optional[Console] = None):
        super().__init__(pos=pos, char="&", color=(240, 100, 100), name="<Camera>")
        self.entity = entity
        self.console = console

    @classmethod
    def from_entity(cls, entity: Entity) -> Camera:
        return Camera(entity.pos, entity)

    def follow(self, console: Optional[console] = None, entity: Optional[Entity] = None) -> None:
        if not console: console = self.console
        else: self.console = console

        # Sets the Camera to follow a new Entity if provided, 
        # and then updates the Camera's location to the location of the followed Entity.
        if entity: self.entity = entity
        if not hasattr(self, "entity"): raise AttributeError("Camera is not following any Entity.")
        self.pos = self.entity.pos

    def console_to_game_map(self, pos: Tuple[int, int] = (0, 0), console: Optional[Console] = None) -> Tuple[int, int]:
        if not console: console = self.console
        else: self.console = console

        # Takes a position relative to the console and returns it's position on the gamemap.
        zero = calculator.tuple_subtract(self.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_add(pos, zero)
    
    def game_map_to_console(self, pos: Tuple[int, int] = (0, 0), console: Optional[Console] = None) -> Tuple[int, int]:
        if not console: console = self.console
        else: self.console = console

        # Takes a position relative to the game map and returns it's position on the console.
        offset = calculator.tuple_subtract(self.pos, (int(console.width / 2), int(console.height / 2)))
        return calculator.tuple_subtract(pos, offset)

    def render(self, console: Optional[Console] = None) -> None:
        if not console: console = self.console
        else: self.console = console

        # Draws a visual representation of the Camera on the console.
        x, y = self.game_map_to_console(self.pos, console)
        console.print(x + 1, y - 1, "L", fg = self.color)
        console.print(x + 2, y - 2, self.char, fg = self.color)