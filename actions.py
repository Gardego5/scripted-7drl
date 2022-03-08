from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

import calculator

class Action:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.game_map.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.
        
        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction (Action):
    def perform(self) -> None:
        raise SystemExit()

class WaitAction (Action):
    def perform(self) -> None:
        pass

class ActionWithDirection (Action):
    def __init__(self, entity: Entity, delta: Tuple[int, int]) -> None:
        super().__init__(entity)

        self.delta = delta

    @property
    def dest(self):
        return calculator.tuple_add(self.entity.pos, self.delta)

    @property
    def target(self):
        return self.engine.game_map.get_blocking_entity_at_location(self.dest)

class MeleeAction (ActionWithDirection):
    def perform(self) -> None:
        if not self.target:
            return 
        
        print(f"The {self.entity.name} kicks the {self.target.name}.")

class MovementAction (ActionWithDirection):
    def perform(self) -> None:
        if not self.engine.game_map.in_bounds(self.dest):
            return  # Destination out of bounds.
        if not self.engine.game_map.tiles["walkable"][self.dest]:
            return  # Destination not walkable.
        if self.engine.game_map.get_blocking_entity_at_location(self.dest):
            return
        
        self.entity.move(self.delta)

class BumpAction (ActionWithDirection):
    def perform(self):
        if self.engine.game_map.get_blocking_entity_at_location(self.dest):
            return MeleeAction(self.entity, self.delta).perform()
        else:
            return MovementAction(self.entity, self.delta).perform()
