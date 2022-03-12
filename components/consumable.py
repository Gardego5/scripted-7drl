from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from input_handlers import ActionOrHandler, RangedAttackSelector, AreaRangedAttackSelector
from actions import ItemAction
import components.ai
import color
from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable (BaseComponent):
    def __init__(self, uses: int = 1, rechargeable: bool = False) -> None:
        self._uses = uses
        self.rechargeable = rechargeable

    @property
    def uses(self) -> int:
        return self._uses
    
    def consume(self) -> None:
        self._uses -= 1
        if self._uses < 1 and self.rechargeable == False:
            self.entity.container.delete(self.entity)

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        return ItemAction(consumer, self.entity)
    
    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError()


class HealingConsumable (Consumable):
    def __init__(
        self, 
        amount: int, 
        *, 
        uses: int = 1,
    ) -> None:
        super().__init__(uses)
        self.amount = amount

    def activate(self, action: ItemAction) -> None:
        if self.uses > 0:
            consumer = action.entity
            amount_recovered = consumer.fighter.heal(self.amount)
        else:
            raise Impossible("This has already been completely used.")

        if amount_recovered > 0:
            if consumer == action.engine.player:
                self.engine.message_log.add_message(
                    f"You consume the {action.item.name}, and recover {amount_recovered} HP!",
                    color.health_recovered,
                )
            else:
                self.engine.message_log.add_message(
                    f"The {consumer.name} consumes the {action.item.name}, and recovers {amount_recovered} HP!",
                    color.health_recovered,
                )
            self.consume()
        else:
            raise Impossible("Your health is already full")


class LightningDamageConsumable (Consumable):
    def __init__(
        self, 
        damage: int,
        maximum_range: int,
        *, 
        uses: int = 1,
    ) -> None:
        super().__init__(uses)
        self.damage = damage
        self.maximum_range = maximum_range
    
    def activate(self, action: ItemAction):
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and action.engine.game_map.visible[actor.pos]:
                distance = consumer.distance(actor.pos)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(f"A lightning bolt strikes the {target.name} with a loud thunderous crack, dealing {self.damage} damage!")
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("No enemy is close enough to strike")


class ConfusionConsumable (Consumable):
    def __init__(
        self, 
        turns: int, 
        chance: float = 1.0,
        *,
        uses: int = 1,
    ) -> None:
        super().__init__(uses)
        self.turns = turns

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        self.engine.message_log.add_message("Select a target location.", color.needs_target)
        return RangedAttackSelector(self.engine, lambda pos: ItemAction(consumer, self.entity, pos))

    def activate(self, action: ItemAction) -> None:
        if not self.engine.game_map.visible[action.target_pos]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not action.target_actor:
            raise Impossible("You must select an enemy to target.")
        if action.target_actor is action.entity:
            raise Impossible("You cannot target yourself.")

        action.target_actor.ai = components.ai.ConfusedEnemy(entity = action.target_actor, previous_ai = action.target_actor.ai, turns = self.turns)
        self.consume()


class FireballDamageConsumable (Consumable):
    def __init__(
        self, 
        damage: int, 
        radius: int,
        *,
        uses: int = 1,
    ) -> None:
        super().__init__(uses)

        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        self.engine.message_log.add_message("Select a target location.", color.needs_target)
        return AreaRangedAttackSelector(self.engine, lambda pos: ItemAction(consumer, self.entity, pos), self.radius)
    
    def activate(self, action: ItemAction) -> None:
        if not self.engine.game_map.visible[action.target_pos]:
            raise Impossible("You cannot target an are that you cannot see.")
        
        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(action.target_pos) <= self.radius:
                self.engine.message_log.add_message(f"The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!")
                actor.fighter.take_damage(self.damage)
                targets_hit = True
            
        if not targets_hit:
            raise Impossible("There are no targets in the radius.")

        self.consume()
