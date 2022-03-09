import tcod.event

# Keybinds for Main Game
MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

PICKUP_KEY = {
    tcod.event.K_g,
}

INVENTORY_KEY = {
    tcod.event.K_i,
}

QUIT_KEYS = {
    tcod.event.K_ESCAPE,
    tcod.event.K_q,
}

OPEN_HISTORY_VIEWER_KEYS = {
    tcod.event.K_v,
}

# Keybinds for Menus
CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1, 
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}

CURSOR_BEGINNING_KEYS = {
    tcod.event.K_HOME,
}

CURSOR_END_KEYS = {
    tcod.event.K_END,
}

CURSOR_SELECT_KEYS = {
    tcod.event.K_RETURN,
}