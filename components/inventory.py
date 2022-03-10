from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Entity, Actor, Item


class Inventory (BaseComponent):
    entity: Entity

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []
    
    def drop(self, item: Item, pos: Tuple[int, int]) -> None:
        item.place(pos, item.ancestor)

        if self.entity == self.engine.player:
            self.engine.message_log.add_message(f"You drop the {item.name}.")
        else:
            self.engine.message_log.add_message(f"The {self.entity.name} drops the {item.name}.")
    
    def delete(self, item: Item):
        self.items.remove(item)
        del item.parent