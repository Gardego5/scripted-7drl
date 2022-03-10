from components.ai import HostileEnemy
from components.fighter import Fighter
from components.consumable import HealingConsumable
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
    char="#", color=(255, 255, 255), name="Player", 
    blocks_movement=True, ai_cls=HostileEnemy, 
    fighter=Fighter(hp=800, defence=1, power=5),
    inventory=Inventory(20),
)

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
    consumable=HealingConsumable(amount=7)
)

bag = Item(
    char=chr(0xC5), color=(190, 150, 230), name="Bag",
    inventory = Inventory(3),
)

health_potion.spawn().container = bag.inventory

bagged_bag = bag.spawn()
bag.spawn().container = bagged_bag.inventory

for i in range(6): bagged_bag.spawn().container = player.inventory

enemies = [
    scientist,
    janitor,
]
enemies_weights = [
    0.3,
    0.7,
]

items = [
    health_potion,
    bag,
]
items_weights = [
    1,
    2,
]
