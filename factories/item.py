from components import consumable
from components.inventory import Inventory
from entity import Item
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
for i in range(3): health_potion.spawn().container = bag.inventory

distribution = {
    0.6: health_potion,
    0.3: bag,
    0.2: lightning_scroll,
    0.2: confusion_scroll,
    1.5: fireball_scroll,
}