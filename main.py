from asyncio import events
from html import entities
import tcod

import color
from engine import Engine
from procgen import generate_dungeon
import entity_factories
from tile_types import SHROUD

def main() -> None:
    screen_width = 80 
    screen_height = 60

    map_width = 80
    map_height = 80

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = entity_factories.player.spawn()

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(map_width, map_height, engine=engine)

    engine.update_fov()
    
    engine.message_log.add_message("You boot up.", color.welcome_text)
    engine.message_log.add_message("Wait; You boot up?!", color.welcome_text)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="YART",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear(SHROUD["ch"], SHROUD["fg"], SHROUD["bg"])
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            
            engine.event_handler.handle_events(context)


if __name__ == "__main__":
    main()