from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
from tcod import Console

from actions import Action, EscapeAction, BumpAction, WaitAction
import keybinds
import color
import exceptions

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


class MainGameEventHandler (EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key in keybinds.MOVE_KEYS:
            delta = keybinds.MOVE_KEYS[key]
            action = BumpAction(self.player, delta)
        elif key in keybinds.WAIT_KEYS:
            action = WaitAction(self.player)
        elif key in keybinds.QUIT_KEYS:
            action = EscapeAction(self.player)
        elif key in keybinds.OPEN_HISTORY_VIEWER_KEYS:
            self.engine.event_handler = HistoryViewer(self.engine)
        
        return action


class GameOverEventHandler (EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in keybinds.QUIT_KEYS:
            raise SystemExit()

class HistoryViewer (EventHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
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
            self.engine.event_handler = MainGameEventHandler(self.engine)