from __future__ import annotations

from typing import List, TYPE_CHECKING

import color
from components.base_component import BaseComponent
from components.inventory import Inventory
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter (BaseComponent):
    entity: Actor

    def __init__(
        self,
        hp: int,
        defence: int,
        power: int,
        luck: int = 0,
        equipment: Inventory = None
    ) -> None:
        self.max_hp = hp
        self._hp = hp
        self.defence = defence
        self.power = power
        self.luck = luck
        if equipment:
            self.equipment = equipment
        else:
            self.equipment = Inventory(0)

    @property
    def equipment(self) -> List[Item]:
        return [slot.inventory.items[0] for slot in self._inventory.items if len(slot.inventory.items) > 0]
    @equipment.setter
    def equipment(self, equipment: Inventory) -> None:
        self._inventory = equipment

    @property
    def hp(self) -> int:
        return self._hp
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self.hp  == 0 and self.entity.ai:
            self.die()

    @property
    def max_hp(self) -> int:
        eq_max_hp = 0
        for eq in self.equipment:
            eq_max_hp += eq.equipable.max_hp

        return self._max_hp + eq_max_hp
    @max_hp.setter
    def max_hp(self, max_hp: int) -> None:
        self._max_hp = max_hp

    @property
    def defence(self) -> int:
        eq_defence = 0
        for eq in self.equipment:
            eq_defence += eq.equipable.defence

        return self._defence + eq_defence
    @defence.setter
    def defence(self, defence: int) -> None:
        self._defence = defence

    @property
    def power(self) -> int:
        eq_power = 0
        for eq in self.equipment:
            eq_power += eq.equipable.power

        return self._power + eq_power
    @power.setter
    def power(self, power: int) -> None:
        self._power = power

    @property
    def luck(self) -> int:
        eq_luck = 0
        for eq in self.equipment:
            eq_luck += eq.equipable.luck

        return self._luck + eq_power
    @luck.setter
    def luck(self, luck: int) -> None:
        self._luck = luck

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount
        
        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp
        
        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message, death_message_color = "You died!", color.player_die
        else:
            death_message, death_message_color = f"{self.entity.name} is dead!", color.enemy_die
        
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
