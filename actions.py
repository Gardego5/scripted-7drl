from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import calculator
import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor


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
            raise exceptions.Impossible("Nothing to attack.") 
        
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
        if not self.engine.game_map.in_bounds(self.dest) or \
            not self.engine.game_map.tiles["walkable"][self.dest] or \
            self.target_blocking_entity:
            raise exceptions.Impossible("That way is blocked")
        
        self.entity.move(self.delta)


class BumpAction (ActionWithDirection):
    def perform(self):
        if self.target_actor:
            return MeleeAction(self.entity, self.delta).perform()
        else:
            return MovementAction(self.entity, self.delta).perform()


class ItemAction (Action):
    def __init__(
        self, 
        entity: Actor,
        item: Item,
        target_pos: Optional[Tuple[int, int]] = None
    ) -> None:
        super().__init__(entity)
        self.item = item
        if not target_pos: target_pos = entity.pos
        self.target_pos = target_pos
    
    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(self.target_pos)
    
    def perform(self) -> None:
        try:
            self.item.consumable.activate(self)
        except AttributeError:
            raise exceptions.Impossible("This item is not consumable.")


class PickupAction (Action):
    # Pickup an Item and add it to the inventory, if there is room for it.
    def perform(self) -> None:
        for item in self.engine.game_map.items:
            if self.entity.pos == item.pos:
                if hasattr(self.entity, "inventory"):
                    if len(self.entity.inventory.items) >= self.entity.inventory.capacity:
                        if self.entity is self.engine.player:
                            raise exceptions.Impossible("Your inventory is full.")
                        else:
                            raise exceptions.Impossible(f"The {self.entity.name}'s inventory is full.")
                    else:
                        item.container = self.entity.inventory
                        if self.entity is self.engine.player:
                            self.engine.message_log.add_message(f"You picked up the {item.name}.")
                            return
                else:
                    if self.entity is self.engine.player:
                        raise exceptions.Impossible("You have no inventory.")
                    else:
                        raise exceptions.Impossible(f"The {self.entity.name} has no inventory.")