from __future__ import annotations

from typing import Union, Optional, List, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod
from tcod.map import compute_fov
import random

from actions import Action, MeleeAction, MovementAction, WaitAction, BumpAction
import calculator

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):
    def __init__(self, target: Optional[Union[Actor, Tuple[int, int]]] = None, tenacity: int = 10):
        self.tenacity = tenacity

        self.path: List[Tuple[int, int]] = []
        if target:
            self.target = target
    
    entity: Actor

    @property
    def target(self) -> Optional[Union[Actor, Tuple[int, int]]]:
        if hasattr(self, "_target"):
            return self._target
        else:
            return None
    @target.setter
    def target(self, target: Optional[Union[Actor, Tuple[int, int]]]) -> None:
        self._target = target
    @property
    def target_pos(self) -> Optional[Tuple[int, int]]:
        if self.target is None:
            return None
        elif isinstance(self.target, tuple):
            return self.target
        else:
            return self.target.pos

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
    
    def can_see(self, target: Tuple[int, int]) -> bool:
        return compute_fov(
            self.engine.game_map.tiles["transparent"],
            (self.entity.x, self.entity.y),
            radius=int(self.entity.fighter.view_distance),
            algorithm=tcod.FOV_SHADOW,
        )[target]

    def get_random_target(self) -> Tuple[int, int]:
        x, y = self.entity.pos

        for i in range(8):
            target_pos = random.randint(x - 5, x + 5), random.randint(y - 5, y + 5)
            try:
                if self.entity.distance(target_pos) > 4 and self.entity.game_map.tiles[target_pos]["walkable"]:
                    return target_pos
            except IndexError:
                pass

        return None
    
    def should_move_away_from_walls(self) -> Optional[Action]:
        x, y = self.entity.pos
        if not self.engine.game_map.tiles[x, y + 1]["walkable"] and not self.engine.game_map.tiles[x, y - 1]["walkable"] and self.engine.game_map.tiles[x - 1, y]["walkable"]:
            return MovementAction(self.entity, (-1, 0))
        if not self.engine.game_map.tiles[x, y + 1]["walkable"] and not self.engine.game_map.tiles[x, y - 1]["walkable"] and self.engine.game_map.tiles[x + 1, y]["walkable"]:
            return MovementAction(self.entity, (1, 0))
        if not self.engine.game_map.tiles[x + 1, y]["walkable"] and not self.engine.game_map.tiles[x - 1, y]["walkable"] and self.engine.game_map.tiles[x, y - 1]["walkable"]:
            return MovementAction(self.entity, (0, -1))
        if not self.engine.game_map.tiles[x + 1, y]["walkable"] and not self.engine.game_map.tiles[x - 1, y]["walkable"] and self.engine.game_map.tiles[x, y + 1]["walkable"]:
            return MovementAction(self.entity, (0, 1))
        return None


class IdleEnemy (BaseAI):
    def perform(self) -> None:
        if self.can_see(self.engine.player.pos):
            return self.give_control(HostileEnemy(self.engine.player.pos))
        elif self.entity.distance(self.engine.player.pos) < self.entity.fighter.earshot:
            return self.give_control(HostileEnemy(target=calculator.tuple_add(self.engine.player.pos, (random.randint(-5, 5), random.randint(-5, 5)))))
        elif random.random() > calculator.lucky_chance(0.8, self.tenacity):
            return self.give_control(MeanderingEnemy())
        else:
            return WaitAction(self.entity).perform()


class MeanderingEnemy (BaseAI):
    def perform(self) -> None:
        if self.can_see(self.engine.player.pos):
            return self.give_control(HostileEnemy(self.engine.player))
        elif self.entity.distance(self.engine.player.pos) < self.entity.fighter.earshot:
            return self.give_control(HostileEnemy(target=calculator.tuple_add(self.engine.player.pos, (random.randint(-5, 5), random.randint(-5, 5)))))
        elif self.target_pos:
            self.path = self.get_path_to(self.target_pos)

            if self.path:
                dest = self.path.pop(0)
                return MovementAction(self.entity, calculator.tuple_subtract(dest, self.entity.pos)).perform()
        else:
            self.target = self.get_random_target()


class HostileEnemy (BaseAI):
    def perform(self) -> None:
        if self.can_see(self.engine.player.pos):
            self.target = self.engine.player

        if self.target:
            delta = calculator.tuple_subtract(self.target_pos, self.entity.pos)
            distance = max(abs(delta[0]), abs(delta[1]))

            if distance <= 1:
                return MeleeAction(self.entity, delta).perform()
                
            self.path = self.get_path_to(self.target_pos)
            
            if self.path:
                dest = self.path.pop(0)
                return MovementAction(self.entity, calculator.tuple_subtract(dest, self.entity.pos)).perform()
        else:
            self.give_control(IdleEnemy())


class ConfusedEnemy (BaseAI):
    def __init__(self, previous_ai: Optional[BaseAI], turns: int, chance: float = 0.90) -> None:
        super().__init__()

        self.previous_ai = previous_ai
        self.turns_remaining = turns
        self.chance = chance
    
    def perform(self) -> None:
        if self.turns_remaining <= 0:  # If the entity has been confused for long enough, stop it's confusion.
            self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            self.give_control(self.previous_ai)
        elif random.random() > self.chance:  # The entity lucked out, and had a coherent thought for a moment.
            return self.previous_ai.perform()
        else:  # The entity stumbles about.
            self.turns_remaining -= 1

            return BumpAction(self.entity, calculator.random_direction()).perform()
