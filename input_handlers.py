from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction, WaitAction
import keybinds

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor

class EventHandler (tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        return NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    @property
    def player(self) -> Actor:
        return self.engine.player


class MainGameEventHandler (EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue
                
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()

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
        
        return action


class GameOverEventHandler (EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key in keybinds.QUIT_KEYS:
            action = EscapeAction(self.player)
        
        return action