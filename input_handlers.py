from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction
import keybinds

if TYPE_CHECKING:
    from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue
                
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key in keybinds.up:
            action = BumpAction(player, (0, -1))
        elif key in keybinds.down:
            action = BumpAction(player, (0, 1))
        elif key in keybinds.left:
            action = BumpAction(player, (-1, 0))
        elif key in keybinds.right:
            action = BumpAction(player, (1, 0))

        elif key in keybinds.escape:
            action = EscapeAction(player)
        
        return action
