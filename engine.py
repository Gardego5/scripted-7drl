from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from entity import Actor, Camera
from game_map import GameMap
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_health_bar, render_names_at_mouse_location

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
        self.mouse_location = (0, 0)
        self.player = player
        self.message_log = MessageLog()
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
    
    def render(self, console: Console) -> None:
        # Render Game Map
        self.game_map.render(console, self.camera)

        # Render UI Elements
        render_health_bar(console, self.player.fighter.hp, self.player.fighter.max_hp)
        render_names_at_mouse_location(console, 2, console.height - 5, self)
        self.message_log.render(console, console.width - 42, console.height - 5, 40, 5)