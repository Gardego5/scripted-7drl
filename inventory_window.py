from typing import Iterable, List, Optional, Reversible, Tuple, TYPE_CHECKING
import textwrap

from tcod import Console

from entity import Item
from components.inventory import Inventory
import color


class InventoryWindow:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.x, self.y, self.width, self.height = 3, 31, 33, 16
        self.cursor = 0

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

    @property
    def render_mode(self) -> Tuple[Iterable[Tuple[str, Item]], int]:
        # Listings short enought to display without wrap.
        if len(self.listings) < self.height:
            return self.listings[:min(len(self.listings), self.height)], self.cursor

        # Cursor at first half of wrapped listings displayed.
        elif self.cursor < int(self.height / 2):
            return self.listings[:min(len(self.listings), self.height)], self.cursor

        # Cursor at second half of wrapped listings displayed.
        elif self.cursor > len(self.listings) - int(self.height / 2):
            return self.listings[-min(len(self.listings), self.height):], self.cursor + self.height - len(self.listings)

        # Cursor in the middle of wrapped listings displayed.
        else:
            return self.listings[self.cursor - int(self.height / 2):self.cursor + int(self.height / 2)], int(self.height / 2)

    def render(self, console: Console, cursor: Optional[int] = None) -> None:
        # Save the cursor if one is provided
        if cursor is not None: self.cursor = cursor

        displayed_listings, selected = self.render_mode

        for i, (listing, item) in enumerate(displayed_listings):
            if i == selected:
                console.print(self.x, self.y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
            else:
                console.print(self.x, self.y + i, listing, fg = item.color, bg = color.ui_bg)