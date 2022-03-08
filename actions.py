from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import calculator
import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Actor) -> None:
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
    def __init__(self, entity: Actor, delta: Tuple[int, int]) -> None:
        super().__init__(entity)

        self.delta = delta

    @property
    def dest(self):
        return calculator.tuple_add(self.entity.pos, self.delta)

    @property
    def target_blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_blocking_entity_at_location(self.dest)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(self.dest)

class MeleeAction (ActionWithDirection):
    def perform(self) -> None:
        if not self.target_actor:
            return 
        
        damage = self.entity.fighter.power - self.target_actor.fighter.defence

        attack_desc = f"{self.entity.name} attacks {self.target_actor.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            self.target_actor.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)

class MovementAction (ActionWithDirection):
    def perform(self) -> None:
        if not self.engine.game_map.in_bounds(self.dest):
            return  # Destination out of bounds.
        if not self.engine.game_map.tiles["walkable"][self.dest]:
            return  # Destination not walkable.
        if self.target_blocking_entity:
            return
        
        self.entity.move(self.delta)

class BumpAction (ActionWithDirection):
    def perform(self):
        if self.target_actor:
            return MeleeAction(self.entity, self.delta).perform()
        else:
            return MovementAction(self.entity, self.delta).perform()
