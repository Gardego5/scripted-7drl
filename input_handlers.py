from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
from tcod import Console

from actions import Action, EscapeAction, BumpAction, WaitAction, PickupAction
import keybinds
import color
import exceptions
import graphics
import render_functions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor
    from inventory_window import InventoryWindow

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
    hover_zones = {
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

    def __init__(self, previous: EventHandler):
        super().__init__(previous)
        self.cursor = 0
        self.window = "Inventory"

    @property
    def inventory_window(self) -> InventoryWindow:
        return self.engine.inventory_window

    def on_render(self, console: Console) -> None:
        player = self.engine.player

        # Draw Normal UI Elements
        render_functions.render_health_bar(console, player.fighter.hp, player.fighter.max_hp)

        # Draw Hardware Screen
        console.rgb[5:34,5:26] = graphics.hardware

        # Draw Inventory Screen
        if self.window == "Inventory":
            self.inventory_window.render(console, self.cursor)
        else: 
            self.inventory_window.render(console)

        # Draw Software Screen
        console.draw_frame(38, 2, 24, 46, title="Software")

        # Draw Help Screen
        # TODO: Draw Help Screen

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in keybinds.CURSOR_Y_KEYS:
            adjust = keybinds.CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                self.cursor = len(self.inventory_window.listings) - 1
            elif adjust > 0 and self.cursor == len(self.inventory_window.listings) - 1:
                self.cursor = 0
            else:
                self.cursor = max(0, min(self.cursor + adjust, len(self.inventory_window.listings) - 1))
        elif event.sym in keybinds.QUIT_KEYS:
            self.close_menu()

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        under_mouse = None
        try: under_mouse = self.hover_zones[event.tile]
        except KeyError: pass
        try: under_mouse = self.inventory_window.hover_zones(event.tile)
        except KeyError: pass
        if under_mouse == None: under_mouse = event.tile
        print(under_mouse)