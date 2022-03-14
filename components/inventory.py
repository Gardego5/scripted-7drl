from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING, Union, Callable

from components.base_component import BaseComponent
import exceptions

if TYPE_CHECKING:
    from entity import Entity, Actor, Item


class Inventory (BaseComponent):
    entity: Entity

    def __init__(self, initialize: Union[int, List[Item]]) -> None:
        self.items: List[Item] = []
        if isinstance(initialize, int):
            self.capacity = initialize
        elif isinstance(initialize, list):
            self.capacity = len(initialize)
            for item in initialize:
                self.add(item)
    
    def drop(self, item: Item, pos: Tuple[int, int]) -> None:
        if item.droppable:
            item.place(pos, item.ancestor)
        else:
            raise exceptions.Impossible("You cannot drop this.")

        if self.entity == self.engine.player:
            self.engine.message_log.add_message(f"You drop the {item.name}.")
        else:
            self.engine.message_log.add_message(f"The {self.entity.name} drops the {item.name}.")
    
    def delete(self, item: Item) -> None:
        self.items.remove(item)
        del item.parent
    
    def add(self, item: Item) -> None:
        if len(self.items) < self.capacity:
            item.container = self
        else:
            raise exceptions.Impossible("Not enough space")


class TypedInventory (Inventory):
    def __init__(self, initialize: Union[int, List[Item]], reqs: set) -> None:
        super().__init__(initialize)

        self.reqs = reqs

    def add(self, item: Item) -> None:    
        if hasattr(item, "flags"):
            if self.reqs.issubset(item.flags):
                super().add(item)
                return

        raise exceptions.Impossible(f"You cannot put {item.name} in {self.name}.")


class DynamicInventory (TypedInventory):
    def __init__(self, capacity_func: Callable[[Inventory], int], reqs: set) -> None:
        self.items: List[Item] = []
        self.capacity_func = capacity_func
        self.reqs = reqs
    
    @property
    def capacity(self) -> int:
        return self.capacity_func(self)
