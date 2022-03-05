from html import entities
from typing import Set, Iterable, Any
from numpy import isin

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities : Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)
    
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console, self.player.x, self.player.y)

        for entity in self.entities:
            if entity == self.player:
                console.print(int(console.width/2), int(console.height/2), entity.char, fg=entity.color)
            else:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear(bg=(0, 0, 100))