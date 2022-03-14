from components.ai import HostileEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Player
import factories.dev

# Player
player = Player(
    fighter=Fighter(
        hp=800, defence=1, power=5, 
        equipment=Inventory(factories.dev.hardware)
    ),
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

distribution = {
    0.3: scientist,
    0.7: janitor,
}