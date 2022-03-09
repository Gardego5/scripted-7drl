from typing import Iterable, List, Optional, Reversible, Tuple, TYPE_CHECKING
import textwrap

from tcod import Console

from entity import Item
from components.inventory import Inventory
import color


class InventoryWindow:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory

    @staticmethod
    def format_listing(item: Item, layer: int = 0) -> Iterable[Tuple[str, Item]]:
        formated_listings = []

        formated_listings.append((f"{' '*layer}{'>'*bool(layer)}{item.name}", item))
        if hasattr(item, "inventory"):
            for sub_item in item.inventory.items:
                formated_listings.extend(InventoryWindow.format_listing(sub_item, layer = layer + 1))

        return formated_listings
    
    def render(
        self, console: Console, x: int, y: int, width: int, height: int, cursor: Optional[int] = None,
    ) -> None:
        listings = []

        for item in self.inventory.items:
            listings.extend(self.format_listing(item))

        if len(listings) < height:
            for i, (listing, item) in enumerate(listings):
                if cursor == i:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
                else:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg)