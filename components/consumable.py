from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable (BaseComponent):
    item: Item

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        return actions.ItemAction(consumer, self.item)
    
    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError()

class HealingConsumable (Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            if consumer == action.engine.player:
                self.engine.message_log.add_message(
                    f"You consume the {self.item.name}, and recover {amount_recovered} HP!",
                    color.health_recovered,
                )
            else:
                self.engine.message_log.add_message(
                    f"The {consumer.name} consumes the {self.item.name}, and recovers {amount_recovered} HP!",
                    color.health_recovered,
                )
        else:
            raise Impossible("Your health is already full")