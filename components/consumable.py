from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
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
    
    def use(self) -> None:
        self._uses -= 1
        if self._uses < 1 and self.rechargeable == False:
            self.entity.container.delete(self.entity)

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        return actions.ItemAction(consumer, self.entity)
    
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

    def activate(self, action: actions.ItemAction) -> None:
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
            self.use()
        else:
            raise Impossible("Your health is already full")