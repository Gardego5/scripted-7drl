from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from entity import Actor, Camera
from game_map import GameMap
from input_handlers import MainGameEventHandler
from render_functions import render_bar
from tile_types import SHROUD

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    game_map: GameMap

    def __init__(
        self,
        player: Actor,
    ) -> None:
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.camera = Camera.from_entity(player)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()
    
    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible
    
    def render(self, console: Console, context: Context) -> None:
        self.camera.follow()

        self.game_map.render(console, self.camera)

        render_bar(console.width - 2, 1, console, current_value=self.player.fighter.hp, maximum_value=self.player.fighter.max_hp, total_size=20, horizontal=False)

        context.present(console)

        console.clear(SHROUD["ch"], SHROUD["fg"], SHROUD["bg"])