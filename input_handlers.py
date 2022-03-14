from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING, Callable, Tuple, Union

import tcod.event
from tcod import Console

import actions
from inventory_window import HardwareWindow, InventoryWindow, SoftwareWindow
import keybinds
import color
import exceptions
import render_functions
import entity

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


ActionOrHandler = Union[actions.Action, "BaseEventHandler"]


class BaseEventHandler (tcod.event.EventDispatch[actions.Action]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, actions.Action), f"{self!r} cannot handle actions."
        return self
    
    def on_render(self, console: Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit()) -> Optional[actions.Action]:
        raise SystemExit()


class EventHandler (BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            return MainGameEventHandler(self.engine)
        return self

    def handle_action(self, action: Optional[actions.Action]) -> bool:
        # Handles actions returned from event methods.
        # Will return true if advances a turn.
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions

        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile):
            self.engine.mouse_location = event.tile
    
    def on_render(self, console: Console) -> None:
        self.engine.camera.follow(console)  # Update the camera's position
        self.engine.render(console)  # Render everything

    @property
    def player(self) -> Actor:
        return self.engine.player


class Menu (EventHandler):
    """Handles user input for actions which require special input."""

    previous: EventHandler = None

    def __init__(self, engine: Engine, previous: Optional[EventHandler] = None):
        super().__init__(engine)
        if previous: self.previous = previous

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        if event.sym in {  # Ignore modifier keys.
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_render(self, console: Console):
        if self.previous:
            self.previous.on_render(console)
        else:
            MainGameEventHandler.on_render(self, console)

    def on_exit(self) -> Optional[ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.
        Returns previous if it was given, otherwise returns to MainGameEventHandler.
        """
        if self.previous:
            return self.previous
        else:
            return MainGameEventHandler(self.engine)


class MainGameEventHandler (EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        if event.sym in keybinds.QUIT_KEYS:
            raise SystemExit()
        if (event.sym in {tcod.event.K_PERIOD, tcod.event.K_COMMA} and event.mod 
            and (tcod.event.KMOD_LSHIFT or tcod.event.KMOD_RSHIFT)):
            return actions.StairsAction(self.player)
        if event.sym in keybinds.MOVE_KEYS:
            return actions.BumpAction(self.player, keybinds.MOVE_KEYS[event.sym])
        if event.sym in keybinds.HISTORY_VIEWER_KEYS:
            return HistoryViewer(self.engine)
        if event.sym in keybinds.PICKUP_KEY:
            return actions.PickupAction(self.player)
        if event.sym in keybinds.INVENTORY_KEY:
            return InventoryEventHandler(self.engine)
        if event.sym in keybinds.LOOK_VIEWER_KEY:
            return LookHandler(self.engine)
        
        return None


class GameOverEventHandler (EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in keybinds.QUIT_KEYS:
            raise SystemExit()
        elif event.sym in keybinds.HISTORY_VIEWER_KEYS:
            return HistoryViewer(self.engine)

class HistoryViewer (Menu):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(self.engine.message_log.messages)
        self.cursor = self.log_length - 1
    
    def on_render(self, console: Console) -> None:
        super().on_render(console)

        log_console = Console(console.width - 6, console.height - 6)

        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER)

        self.engine.message_log.render_messages(
            log_console, 1, 1, log_console.width - 2, log_console.height - 2, 
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        if event.sym in keybinds.CURSOR_Y_KEYS:
            adjust = keybinds.CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                self.cursor = 0
            else:
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym in keybinds.CURSOR_BEGINNING_KEYS:
            self.cursor = 0
        elif event.sym in keybinds.CURSOR_END_KEYS:
            self.cursor = self.log_length - 1
        else:
            return self.on_exit()
        return None


class InventoryEventHandler (Menu):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.cursor = 0
        self.window = "Inventory"
        self.hardware_window = HardwareWindow(self.player.fighter._inventory)
        self.inventory_window = InventoryWindow(self.player.inventory)
        self.software_window = SoftwareWindow(self.player.active, self.player.passive, self.player.storage)

    @property
    def active_window(self):
        windows = {
            "Hardware": self.hardware_window,
            "Inventory": self.inventory_window,
            "Software": self.software_window,
            "No Window": None,
        }
        return windows[self.window]

    def change_window(self):
        windows = ["Hardware", "Inventory", "Software"]
        if self.window in windows:
            for i, window in enumerate(windows):
                if self.window == window:
                    self.window = windows[i - 1]
                    return
        else:
            self.window = "Inventory"

    def on_render(self, console: Console) -> None:
        super().on_render(console)
        console.draw_frame(2, 2, 76, 46, decoration = "         ", bg = color.ui_bg, fg = color.ui_main)

        player = self.engine.player

        # Draw Normal UI Elements
        render_functions.render_health_bar(console, player.fighter.hp, player.fighter.max_hp)

        # Draw Hardware Screen
        if self.window == "Hardware":
            self.hardware_window.render(console, self.cursor)
        else: 
            self.hardware_window.render(console)

        # Draw Inventory Screen
        if self.window == "Inventory":
            self.inventory_window.render(console, self.cursor)
        else: 
            self.inventory_window.render(console)

        # Draw Software Screen
        if self.window == "Software":
            self.software_window.render(console, self.cursor)
        else: 
            self.software_window.render(console)

        # Draw Description Screen
        console.draw_frame(38, 39, 25, 9, title="Description")
        try:
            console.print_box(39, 40, 23, 7, self.active_window.selected_listing[1].description, fg=color.ui_main)
        except AttributeError:
            console.print_box(39, 40, 23, 7, "Nothing Selected.", fg=color.ui_main)

        # Draw Info Screen
        console.draw_frame(64, 27, 14, 21, title="Info")

        # Draw Keybinds Help
        for i, key_hint in enumerate(["[d] Drop", "[u] Use", "[e] Equip"]):
            console.print(64, 25 - i, key_hint, fg=color.ui_very_subdued)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        # Move the cursor in the selected window, but don't make it out of bounds of the window's listings.
        if event.sym in keybinds.WINDOW_TAB_KEY:
            self.change_window()
            return
        elif self.window == "No Window":
            if event.sym in keybinds.QUIT_KEYS:
                return self.on_exit()
        else:
            if event.sym in keybinds.CURSOR_Y_KEYS:
                adjust = keybinds.CURSOR_Y_KEYS[event.sym]
                if adjust < 0 and self.cursor == 0:
                    self.cursor = len(self.active_window.listings) - 1
                elif adjust > 0 and self.cursor == len(self.active_window.listings) - 1:
                    self.cursor = 0
                else:
                    self.cursor = max(0, min(self.cursor + adjust, len(self.active_window.listings) - 1))
            elif event.sym in keybinds.QUIT_KEYS:
                self.window = "No Window"
                return
            elif event.sym in keybinds.INV_DROP_KEY and self.active_window is self.inventory_window:
                return actions.DropItem(self.player, self.active_window.selected_item)
            elif event.sym in keybinds.INV_USE_KEY and self.active_window in [self.inventory_window, self.software_window]:
                if hasattr(self.inventory_window.selected_item, "consumable"):
                    return self.inventory_window.selected_item.consumable.get_action(self.engine.player)
                else:
                    self.engine.message_log.add_message("You can not use this item that way.", color.impossible)
                    return  # Cannot use impossible exception because not inside action.
            elif event.sym in keybinds.INV_EQUIP_KEY and self.active_window == self.inventory_window:
                if hasattr(self.inventory_window.selected_item, "equipable"):
                    return self.inventory_window.selected_item.equipable.get_action(self.engine.player)
                else:
                    self.engine.message_log.add_message("This item cannot be equiped.", color.impossible)
                    return  # Cannot use impossible exception because not inside action.

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        found_window = False

        for i_window in [self.hardware_window, self.inventory_window, self.software_window]:
            try:
                # If you clicked on a selectable item, then select that item in that window.
                item, cursor = i_window.hover_zones(self.engine.mouse_location)
                self.cursor, self.window = cursor, i_window.title
                found_window = True
            except exceptions.OutOfWindow:
                # Do nothing if you didn't click in a window.
                pass
            except IndexError:
                # If you didn't click on a selectable item, but within a window, select the window,
                # but keep the selected item of that window the same.
                self.cursor, self.window = i_window.cursor, i_window.title
                found_window = True
        if not found_window:
            self.window = "No Window"


class SelectInventorySlotHandler (InventoryEventHandler):
    def __init__(self, engine: Engine, callback: Callable[[entity.Item], actions.Action]) -> None:
        super().__init__(engine)

        self.callback = callback
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        # Move the cursor in the selected window, but don't make it out of bounds of the window's listings.
        if event.sym in keybinds.WINDOW_TAB_KEY:
            self.change_window()
            return
        elif self.window == "No Window":
            if event.sym in keybinds.QUIT_KEYS:
                return self.on_exit()
        else:
            if event.sym in keybinds.CURSOR_Y_KEYS:
                adjust = keybinds.CURSOR_Y_KEYS[event.sym]
                if adjust < 0 and self.cursor == 0:
                    self.cursor = len(self.active_window.listings) - 1
                elif adjust > 0 and self.cursor == len(self.active_window.listings) - 1:
                    self.cursor = 0
                else:
                    self.cursor = max(0, min(self.cursor + adjust, len(self.active_window.listings) - 1))
            elif event.sym in keybinds.QUIT_KEYS:
                self.window = "No Window"
                return
            elif event.sym in keybinds.CURSOR_SELECT_KEYS:
                return self.on_item_selected(self.active_window.selected_item)

    def on_item_selected(self, item: entity.Item) -> Optional[ActionOrHandler]:
        return self.callback(item)


class SelectHandler (Menu):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        self.engine.mouse_location = self.engine.camera.game_map_to_console(self.engine.player.pos)
    
    def on_render(self, console: Console) -> None:
        MainGameEventHandler.on_render(self, console)
        console.rgb["bg"][self.engine.mouse_location] = color.white
        console.rgb["fg"][self.engine.mouse_location] = color.black
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        if event.sym in keybinds.MOVE_KEYS:
            modifier = 1
            for mod in keybinds.MOVE_MODIFIER_KEYS:
                if mod == event.mod:
                    modifier *= keybinds.MOVE_MODIFIER_KEYS[mod]
        
            x, y = self.engine.mouse_location
            dx, dy = keybinds.MOVE_KEYS[event.sym]
            x += dx * modifier
            y += dy * modifier
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            return None
        elif event.sym in keybinds.CURSOR_SELECT_KEYS:
            return self.on_index_selected(self.engine.mouse_location)
        elif event.sym in keybinds.QUIT_KEYS:
            return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        return self.on_index_selected(self.engine.mouse_location)

    def on_index_selected(self, pos: Tuple[int, int]) -> Optional[ActionOrHandler]:
        raise NotImplementedError()


class LookHandler (SelectHandler):
    def on_index_selected(self, pos: Tuple[int, int]) -> Optional[ActionOrHandler]:
        self.on_exit()


class RangedAttackSelector (SelectHandler):
    # Allows selecting a tile. If there are qualms about the tile selected, request a new tile. 
    # If a suitable tile is found, 
    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], actions.Action]) -> None:
        super().__init__(engine)

        self.callback = callback
    
    def on_index_selected(self, pos: Tuple[int, int]) -> Optional[ActionOrHandler]:
        return self.callback(self.engine.camera.console_to_game_map(pos))


class AreaRangedAttackSelector (RangedAttackSelector):
    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], actions.Action], radius: int) -> None:
        super().__init__(engine, callback)
        
        self.radius = radius
    
    def on_render(self, console: Console) -> None:
        super().on_render(console)

        x, y = self.engine.mouse_location

        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )


class PopupMessage (BaseEventHandler):
    def __init__(self, previous: EventHandler, text: str) -> None:
        self.previous = previous
        self.text = text

    def on_render(self, console: Console) -> None:
        self.previous.on_render(console)
        console.tiles["fg"] //= 8
        console.tiles["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg = color.white,
            bg = color.black,
            alignment = tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        return self.previous
    
    def ev_mousebuttondown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        return self.previous
