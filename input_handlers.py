from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction
import keybinds

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key in keybinds.up:
            action = MovementAction((0, -1))
        elif key in keybinds.down:
            action = MovementAction((0, 1))
        elif key in keybinds.left:
            action = MovementAction((-1, 0))
        elif key in keybinds.right:
            action = MovementAction((1, 0))

        elif key in keybinds.escape:
            action = EscapeAction()
        
        return action
