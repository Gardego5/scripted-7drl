import traceback

import tcod

import color
from engine import Engine
import exceptions
import input_handlers
from procgen import generate_dungeon
import entity_factories
from tile_types import SHROUD

def main() -> None:
    screen_width = 80 
    screen_height = 50

    map_width = 80
    map_height = 80

    tileset = tcod.tileset.load_tilesheet(
        "Md_curses_16x16.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    player = entity_factories.player.spawn()

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(map_width, map_height, engine=engine)

    engine.update_fov()
    
    engine.message_log.add_message("You boot up.", color.welcome_text)
    engine.message_log.add_message("Wait; You boot up?!", color.welcome_text)

    handler = input_handlers.MainGameEventHandler(engine)

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
                    engine.message_log.add_message(traceback.format_exc(), color.error)  # Print to message log.
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit or BaseException:
            # TODO: Add the save function here.
            raise


if __name__ == "__main__":
    main()