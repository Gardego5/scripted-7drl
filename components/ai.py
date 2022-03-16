from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod
import random

from actions import Action, MeleeAction, MovementAction, WaitAction, BumpAction
import calculator

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):
    def __init__(self, entity: Actor, tenacity: int = 10):
        self.entity = entity
        self.tenacity = tenacity
    
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.game_map.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.game_map.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.pos]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.pos] += self.tenacity

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root(self.entity.pos)  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to(dest)[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]

class DocileEnemy (BaseAI):
    def perform(self) -> None:
        if self.entity.distance(self.engine.player.pos) < self.entity.fighter.view_distance:
            self.entity.ai = HostileEnemy(self.entity)
        else:
            return WaitAction(self.entity).perform()

class HostileEnemy (BaseAI):
    def __init__(self, entity: Actor, tenacity: int = 10):
        super().__init__(entity, tenacity=tenacity)
        self.path: List[Tuple[int, int]] = []
    
    def perform(self) -> None:
        target = self.engine.player

        delta = calculator.tuple_subtract(target.pos, self.entity.pos)
        distance = max(abs(delta[0]), abs(delta[1]))

        if distance <= 1:
            return MeleeAction(self.entity, delta).perform()
            
        self.path = self.get_path_to(target.pos)
        
        if self.path:
            dest = self.path.pop(0)
            return MovementAction(self.entity, calculator.tuple_subtract(dest, self.entity.pos)).perform()
        
        return WaitAction(self.entity).perform()


class ConfusedEnemy (BaseAI):
    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI], turns: int, chance: float = 0.90) -> None:
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns
        self.chance = chance
    
    def perform(self) -> None:
        if self.turns_remaining <= 0:  # If the entity has been confused for long enough, stop it's confusion.
            self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            self.entity.ai = self.previous_ai
        elif random.random() > self.chance:  # The entity lucked out, and had a coherent thought for a moment.
            return self.previous_ai.perform()
        else:  # The entity stumbles about.
            self.turns_remaining -= 1

            return BumpAction(self.entity, calculator.random_direction()).perform()
