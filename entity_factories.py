from entity import Entity

player = Entity(char="#", color=(255, 255, 255), name="Player", blocks_movement=True)

scientist = Entity(char="S", color=(200, 255, 200), name="Scientist", blocks_movement=True)
janitor = Entity(char="J", color=(179, 113, 55), name="Janitor", blocks_movement=True)

enemies = [
    scientist,
    janitor,
]

enemies_weights = [
    0.3,
    0.7,
]