#!/usr/bin/env python
import traceback

import tcod

import color
import exceptions
import input_handlers
from tile_types import SHROUD
import setup_game


def save_game(handler: input_handlers.BaseEventHandler) -> None:
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as()
        print("Game Saved.")

def main() -> None:
    screen_width = 80 
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "Md_curses_16x16.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="YART",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear(SHROUD["ch"], SHROUD["fg"], SHROUD["bg"])
                handler.on_render(root_console)
                context.present(root_console)
                
                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:
                    traceback.print_exc()  # Print to stderr.
                    handler.engine.message_log.add_message(traceback.format_exc(), color.error)  # Print to message log.
        except SystemExit or BaseException:
            if handler.engine.player.is_alive:
                save_game(handler)


if __name__ == "__main__":
    main()