from __future__ import annotations

from typing import List

import random

from components import consumable
from components.inventory import Inventory
from components.equipable import Equipable
from entity import Item
import factories.modifiers
import calculator
import color

# Items
health_potion = Item(
    char="!", color=(127, 0, 255), name="Health Potion",
    consumable = consumable.HealingConsumable(amount=7),
)

lightning_scroll = Item(
    char="~", color=color.yellow, name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char="~", color=(207, 63, 255), name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(10),
)

fireball_scroll = Item(
    char="~", color=color.bright_orange, name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(9, 3),
)

bag = Item(
    char=chr(0xC5), color=(190, 150, 230), name="Bag",
    inventory = Inventory(3),
)

# Composed Item Configuration
for i in range(3): bag.inventory.add(health_potion.spawn())

# Dynamically Genertated Items
def modify(
    item: Item,
    valid_modifiers: List[factories.modifiers.Modifier],
    level: int,
) -> item:
    modifiers = random.choices(valid_modifiers, k=random.randint(0, 3))

    for modifier in modifiers:
        modifier = modifier(level)
        item.name = " ".join([modifier.name, item.name])
        item.equipable.max_hp = item.equipable.max_hp + modifier.max_hp
        item.equipable.defence = item.equipable.defence + modifier.defence
        item.equipable.power = item.equipable.power + modifier.power
        item.equipable.luck = item.equipable.luck + modifier.luck
        item.equipable.cpu_threads = item.equipable.cpu_threads + modifier.cpu_threads
        item.equipable.apu_threads = item.equipable.apu_threads + modifier.apu_threads
        item.equipable.data_storage = item.equipable.data_storage + modifier.data_storage
        item.equipable.max_shield = item.equipable.max_shield + modifier.max_shield
        item.equipable.shield_threshold = item.equipable.shield_threshold + modifier.shield_threshold
    
    return item

def cpu(
    level: int = 0,
) -> Item:
    item = Item(
        char=chr(0x2261),
        name="CPU",
        flags={"cpu"},
        color=color.leveled(level),
        equipable=Equipable(
            cpu_threads=2 + level // 3,
        ),
    )

    modify(item, factories.modifiers.base_modifiers, level)
    return item

def apu(
    level: int = 0,
    modifier_class: int = 0
) -> Item:
    item = Item(
        char=chr(0x2261),
        name="APU",
        flags={"apu"},
        color=color.leveled(level),
        equipable=Equipable(
            apu_threads=2 + level // 3,
        ),
    )

    modify(item, factories.modifiers.base_modifiers, level)
    return item

distribution = {
    0.5: cpu,
    0.5: apu,
}