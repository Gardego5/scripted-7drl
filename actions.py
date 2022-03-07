from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

import calculator

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.
        
        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction (Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class ActionWithDirection (Action):
    def __init__(self, delta: Tuple[int, int]) -> None:
        super().__init__()

        self.delta = delta

class MeleeAction (ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest = calculator.tuple_add(entity.pos, self.delta)

        target = engine.game_map.get_blocking_entity_at_location(dest)
        if not target:
            return 
        
        print(f"The {entity.name} kicks the {target.name}.")

class MovementAction (ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest = calculator.tuple_add(entity.pos, self.delta)

        if not engine.game_map.in_bounds(dest):
            return  # Destination out of bounds.
        if not engine.game_map.tiles["walkable"][dest]:
            return  # Destination not walkable.
        if engine.game_map.get_blocking_entity_at_location(dest):
            return
        
        entity.move(self.delta)

class BumpAction (ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity):
        dest = calculator.tuple_add(entity.pos, self.delta)

        if engine.game_map.get_blocking_entity_at_location(dest):
            return MeleeAction(self.delta).perform(engine, entity)
        else:
            return MovementAction(self.delta).perform(engine, entity)
