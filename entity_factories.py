from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor

player = Actor(char="#", color=(255, 255, 255), name="Player", blocks_movement=True, ai_cls=HostileEnemy, fighter=Fighter(hp=8, defence=1, power=2))

scientist = Actor(char="S", color=(200, 255, 200), name="Scientist", blocks_movement=True, ai_cls=HostileEnemy, fighter=Fighter(hp=8, defence=1, power=2))
janitor = Actor(char="J", color=(179, 113, 55), name="Janitor", blocks_movement=True, ai_cls=HostileEnemy, fighter=Fighter(hp=13, defence=1, power=4))

enemies = [
    scientist,
    janitor,
]

enemies_weights = [
    0.3,
    0.7,
]