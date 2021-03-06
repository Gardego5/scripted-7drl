from __future__ import annotations

from typing import List, Tuple

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
    modifier_distribution: List[Tuple[factories.modifiers.Modifier, float]],
    level: int,
) -> item:
    modifiers, weights = [], []
    for modifier, weight in modifier_distribution:
        if not bool(modifier.blacklist.intersection(item.flags)):  # Make sure that the item is not in the blacklist.
            if modifier.whitelist:  # If there is a whitelist for the modifier, make sure that the item is in the whitelist.
                if bool(modifier.whitelist.intersection(item.flags)):
                    modifiers.append(modifier)
                    weights.append(weight)
            else:  # If there is no whitelist, add it.
                modifiers.append(modifier)
                weights.append(weight)

    # Picks a weighted random number between 0 and 3 to choose how many modifiers to add.
    modifiers = random.sample(modifiers, random.sample([0, 1, 2, 3], 1, counts=[11, 6, 2, 1])[0], counts = weights)

    for modifier in modifiers:
        modifier = modifier(level)
        item.name = "".join([chr(0xAB), item.name, chr(0xBB)])
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

    modify(item, factories.modifiers.distribution, level)
    return item

def apu(
    level: int = 0,
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

    modify(item, factories.modifiers.distribution, level)
    return item

def gpu(
    level: int = 0,
) -> Item:
    item = Item(
        char=chr(0x2261),
        name="GPU",
        flags={"gpu"},
        color=color.leveled(level),
        equipable=Equipable(
            view_distance=2 + level,
        ),
    )

    modify(item, factories.modifiers.distribution, level)
    return item

distribution = [
    (cpu, 0.5),
    (apu, 0.5),
    (gpu, 0.5),
]