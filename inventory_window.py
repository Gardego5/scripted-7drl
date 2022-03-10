from typing import Iterable, List, Optional, Reversible, Tuple, TYPE_CHECKING
import textwrap

from tcod import Console

from entity import Item
from components.inventory import Inventory
import color
import graphics
import exceptions
import calculator


class InventoryWindow:
    x, y, width, height = 3, 31, 33, 16
    title = "Inventory"

    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.cursor = 0

    def _format_listing(self, item: Item, layer: int = 0) -> Iterable[Tuple[str, Item]]:
        formated_listings = []

        formated_listing = f" {' '*layer}{'>'*bool(layer)}{item.name}"
        formated_listing = formated_listing + " " * (self.width - len(formated_listing))

        formated_listings.append((formated_listing, item))
        if hasattr(item, "inventory"):
            for sub_item in item.inventory.items:
                formated_listings.extend(self._format_listing(sub_item, layer = layer + 1))

        return formated_listings

    @property
    def selected_listing(self) -> Tuple[str, Item]:
        try:
            return self.listings[self.cursor]
        except IndexError:
            if self.cursor > 0:
                self.cursor -= 1
                return self.selected_listing
            else:
                return "", None


    @property
    def selected_item(self) -> Item:
        return self.selected_listing[1]

    @property
    def listings(self) -> Iterable[Tuple[str, Item]]:
        listings = []
        for item in self.inventory.items:
            listings.extend(self._format_listing(item))
        return listings

    @property
    def _render_mode(self) -> Tuple[Iterable[Tuple[str, Item]], int]:
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

    def hover_zones(self, pos: Tuple[int, int]) -> Tuple[Item, int]:
        # Returns the item under the position and it's position in the listings.
        if self.x <= pos[0] < self.x + self.width and self.y <= pos[1] < self.y + self.height:
            displayed_listings, selected = self._render_mode
            displayed_i = pos[1] - self.y
            return displayed_listings[displayed_i][1], displayed_i - selected + self.cursor
        else:
            raise exceptions.OutOfWindow

    def render(self, console: Console, cursor: Optional[int] = None) -> None:
        # Save the cursor if one is provided
        if cursor is not None: self.cursor = cursor

        displayed_listings, selected = self._render_mode

        console.draw_frame(self.x - 1, self.y - 1, self.width + 2, self.height + 2, title=self.title)

        for i, (listing, item) in enumerate(displayed_listings):
            if i == selected:
                console.print(self.x, self.y + i, listing, fg = item.color, bg = color.ui_bg_highlighted)
            else:
                console.print(self.x, self.y + i, listing, fg = item.color, bg = color.ui_bg)


class SoftwareWindow (InventoryWindow):
    x, y, width, height = 39, 3, 23, 34
    title = "Software"


class HardwareWindow (InventoryWindow):
    x, y, width, height = 5, 5, 29, 21
    title = "Hardware"
    item_zones = {
        ( 8,  6): 0,
        ( 9,  6): 0,
        (12,  6): 1,
        (13,  6): 1,
        (16,  6): 2,
        (17,  6): 2,
        (21,  6): 3,
        (22,  6): 3,
        (25,  6): 4,
        (26,  6): 4,
        (29,  6): 5,
        (30,  6): 5,
        ( 9, 16): 6,
        (19, 15): 7,
        (29, 13): 8,
        (31, 19): 9,
        (10, 24): 10,
        (13, 24): 11,
        (16, 24): 12,
        (22, 24): 13,
        (25, 24): 14,
        (28, 24): 15,
    }
    zones = {
        (18, 14): "CPU_desc",
        (19, 14): "CPU_desc",
        (20, 14): "CPU_desc",
        (19, 15): "CPU",
        (28, 12): "APU_desc",
        (29, 12): "APU_desc",
        (30, 12): "APU_desc",
        (29, 13): "APU",
        (30, 18): "GPU_desc",
        (31, 18): "GPU_desc",
        (32, 18): "GPU_desc",
        (31, 19): "GPU",
        ( 8, 13): "PSU_desc",
        ( 9, 13): "PSU_desc",
        (10, 13): "PSU_desc",
        ( 7, 10): "Peripherals",
        ( 8, 10): "Peripherals",
        ( 9, 10): "Peripherals",
        (10, 10): "Peripherals",
        (11, 10): "Peripherals",
        (12, 10): "Peripherals",
        (13, 10): "Peripherals",
        (14, 10): "Peripherals",
        (15, 10): "Peripherals",
        (16, 10): "Peripherals",
        (17, 10): "Peripherals",
        ( 8,  6): "P1",
        ( 9,  6): "P1",
        (12,  6): "P2",
        (13,  6): "P2",
        (16,  6): "P3",
        (17,  6): "P3",
        (21,  6): "P4",
        (22,  6): "P4",
        (25,  6): "P5",
        (26,  6): "P5",
        (29,  6): "P6",
        (30,  6): "P6",
        (22, 21): "Data",
        (23, 21): "Data",
        (24, 21): "Data",
        (25, 21): "Data",
        (10, 24): "D1",
        (13, 24): "D2",
        (16, 24): "D3",
        (22, 24): "D4",
        (25, 24): "D5",
        (28, 24): "D6",
    }

    @property
    def listings(self) -> Iterable[Tuple[str, Item]]:
        return [(item.inventory.items[0].name, item.inventory.items[0]) if len(item.inventory.items) else (item.name, item) for item in self.inventory.items]

    def hover_zones(self, pos: Tuple[int, int]) -> Tuple[Item, int]:
        # Returns the item under the position and it's position in the listings.
        if self.x <= pos[0] < self.x + self.width and self.y <= pos[1] < self.y + self.height:
            if pos in self.item_zones:
                return self.inventory.items[self.item_zones[pos]], self.item_zones[pos]
            else:
                raise IndexError
        else:
            raise exceptions.OutOfWindow

    def render(self, console: Console, cursor: Optional[int] = None) -> None:
        # Save the cursor if one is provided
        if cursor is not None: self.cursor = cursor

        # Print the harware graphic
        console.rgb[5:34,5:26] = graphics.hardware

        # Print the devices
        for i, device in enumerate(self.inventory.items):
            if i == self.cursor:
                bg = color.ui_bg_highlighted
            else:
                bg = color.ui_bg
            if len(device.inventory.items) == 1:
                installed_device = device.inventory.items[0]
                console.print(*device.pos, installed_device.char, fg = installed_device.color, bg = bg)
            else:
                console.print(*device.pos, device.char, fg = device.color, bg = bg)