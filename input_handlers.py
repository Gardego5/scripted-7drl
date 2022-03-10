from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
from tcod import Console

from actions import Action, EscapeAction, BumpAction, WaitAction, PickupAction
from inventory_window import HardwareWindow, InventoryWindow, SoftwareWindow
import keybinds
import color
import exceptions
import render_functions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor

class EventHandler (tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> None:
        self.handle_action(self.dispatch(event))

    def handle_action(self, action: Optional[Action]) -> bool:
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

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def on_render(self, console: Console) -> None:
        self.engine.camera.follow()  # Update the camera's position
        self.engine.render(console)  # Render everything

    @property
    def player(self) -> Actor:
        return self.engine.player


class Menu (EventHandler):
    def __init__(self, previous: EventHandler):
        super().__init__(previous.engine)
        previous.engine.event_handler = self
        self.previous = previous

    def close_menu(self):
        self.engine.event_handler = self.previous


class MainGameEventHandler (EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        if event.sym in keybinds.MOVE_KEYS:
            delta = keybinds.MOVE_KEYS[event.sym]
            action = BumpAction(self.player, delta)
        elif event.sym in keybinds.WAIT_KEYS:
            action = WaitAction(self.player)
        elif event.sym in keybinds.QUIT_KEYS:
            action = EscapeAction(self.player)
        elif event.sym in keybinds.OPEN_HISTORY_VIEWER_KEYS:
            HistoryViewer(self)
        elif event.sym in keybinds.PICKUP_KEY:
            action = PickupAction(self.player)
        elif event.sym in keybinds.INVENTORY_KEY:
            InventoryEventHandler(self)
        
        return action


class GameOverEventHandler (EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in keybinds.QUIT_KEYS:
            raise SystemExit()
        elif event.sym in keybinds.OPEN_HISTORY_VIEWER_KEYS:
            HistoryViewer(self)

class HistoryViewer (Menu):
    def __init__(self, previous: EventHandler):
        super().__init__(previous)
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
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
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
            self.close_menu()


class InventoryEventHandler (Menu):
    def __init__(self, previous: EventHandler):
        super().__init__(previous)
        self.cursor = 0
        self.window = "Inventory"
        self.hardware_window = HardwareWindow(self.player.hardware)
        self.inventory_window = InventoryWindow(self.player.inventory)
        self.software_window = SoftwareWindow(self.player.software)

    @property
    def active_window(self):
        windows = {
            "Hardware": self.hardware_window,
            "Inventory": self.inventory_window,
            "Software": self.software_window,
        }
        return windows[self.window]

    def on_render(self, console: Console) -> None:
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

        # Draw Info Screen
        console.draw_frame(64, 27, 14, 21, title="Info")

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in keybinds.CURSOR_Y_KEYS:
            adjust = keybinds.CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                self.cursor = len(self.active_window.listings) - 1
            elif adjust > 0 and self.cursor == len(self.active_window.listings) - 1:
                self.cursor = 0
            else:
                self.cursor = max(0, min(self.cursor + adjust, len(self.active_window.listings) - 1))
        elif event.sym in keybinds.QUIT_KEYS:
            self.close_menu()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> None:
        for i_window in [self.hardware_window, self.inventory_window, self.software_window]:
            try:
                item, cursor = i_window.hover_zones(self.engine.mouse_location)
                self.cursor, self.window = cursor, i_window.title
            except exceptions.OutOfWindow:
                pass
            except IndexError:
                self.cursor, self.window = i_window.cursor, i_window.title