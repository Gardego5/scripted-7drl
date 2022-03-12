from components.ai import HostileEnemy
from components.fighter import Fighter
from components import consumable
from components.inventory import Inventory
from entity import Actor, Item, Player
import dev
import color

# Player
player = Player(
    fighter=Fighter(hp=800, defence=1, power=5),
    inventory=Inventory(20),
)
for device in dev.hardware:
    device.container = player.hardware
for device in dev.software:
    device.container = player.software

# Enemies
scientist = Actor(
    char="S", color=(200, 255, 200), name="Scientist", 
    blocks_movement=True, ai_cls=HostileEnemy, 
    fighter=Fighter(hp=8, defence=1, power=2),
    inventory=Inventory(3),
)
janitor = Actor(
    char="J", color=(179, 113, 55), name="Janitor", 
    blocks_movement=True, ai_cls=HostileEnemy, 
    fighter=Fighter(hp=13, defence=1, power=4),
    inventory=Inventory(3)
)

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

bag = Item(
    char=chr(0xC5), color=(190, 150, 230), name="Bag",
    inventory = Inventory(3),
)

for i in range(3): health_potion.spawn().container = bag.inventory
bag.spawn().container = player.inventory
confusion_scroll.spawn().container = player.inventory

enemies = {
    0.3: scientist,
    0.7: janitor,
}

items = {
    0.6: health_potion,
    0.3: bag,
    0.2: lightning_scroll,
    1.5: confusion_scroll,
}