from components.ai import HostileEnemy
from components.fighter import Fighter
from components.consumable import HealingConsumable
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
    char="#", color=(255, 255, 255), name="Player", 
    blocks_movement=True, ai_cls=HostileEnemy, 
    fighter=Fighter(hp=8, defence=1, power=2),
    inventory=Inventory(3),
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
]
items_weights = [
    1,
]
