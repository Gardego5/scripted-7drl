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

    @property
    def listings(self) -> Iterable[Tuple[str, Item]]:
        listings = []
        for item in self.inventory.items:
            listings.extend(self.format_listing(item))
        return listings

    def render(
        self, console: Console, x: int, y: int, width: int, height: int, cursor: Optional[int] = None,
    ) -> None:
        if len(self.listings) < height or not cursor:
            for i, (listing, item) in enumerate(self.listings[:min(len(self.listings), height)]):
                if i == cursor:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
                else:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg)
        elif cursor < int(height / 2):
            for i, (listing, item) in enumerate(self.listings[:min(len(self.listings), height)]):
                if i == cursor:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
                else:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg)
        elif cursor > len(self.listings) - int(height / 2):
            for i, (listing, item) in enumerate(self.listings[-min(len(self.listings), height):]):
                if i == cursor + height - len(self.listings):
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
                else:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg)
        else:
            for i, (listing, item) in enumerate(self.listings[cursor - int(height / 2):cursor + int(height / 2)]):
                if i == int(height / 2):
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
                else:
                    console.print(x, y + i, listing, fg = item.color, bg = color.ui_bg)