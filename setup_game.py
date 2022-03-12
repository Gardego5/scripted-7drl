from __future__ import annotations

from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
import input_handlers
import keybinds
from procgen import generate_dungeon


def new_game() -> Engine:
    map_width = 80
    map_height = 80

    player = entity_factories.player.spawn()

    engine = Engine(player)

    engine.game_map = generate_dungeon(map_width, map_height, engine=engine)

    engine.update_fov()
    
    engine.message_log.add_message("You boot up.", color.welcome_text)
    engine.message_log.add_message("Wait; You boot up?!", color.welcome_text)

    return engine

class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 10,
            "SCRIPTED 7drl",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        console.print(
            console.width // 2,
            console.height - 2,
            "Garrett Davis",
            fg=color.menu_author,
            alignment=tcod.CENTER,
        )

        console.print(
            console.width // 2,
            console.height - 6,
            "".join([text.center(24) for text in ["[N] Play a new game", "[Q] Quit", "[C] Continue last game"]]),
            fg=color.menu_text,
            bg=color.black,
            alignment=tcod.CENTER,
            bg_blend=tcod.BKGND_ALPHA(64),
        )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in keybinds.QUIT_KEYS:
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            # TODO: Load the game here
            pass
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
