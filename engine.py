from html import entities
from typing import Set, Iterable, Any
from numpy import isin

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
from tile_types import SHROUD

class Engine:
    def __init__(
        self, 
        event_handler: EventHandler, 
        game_map: GameMap, 
        player: Entity
    ) -> None:
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)

            self.update_fov()
    
    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible
    
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console, self.player.x, self.player.y)

        """
        for entity in self.entities:
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x - self.player.x + int(console.width/2), entity.y - self.player.y + int(console.height/2), entity.char, fg=entity.color)
        """

        context.present(console)

        console.clear(SHROUD["ch"], SHROUD["fg"], SHROUD["bg"])