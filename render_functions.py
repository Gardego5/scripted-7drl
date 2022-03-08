from __future__ import annotations

from typing import Tuple, Optional, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def print_vertical(
    x: int, y: int,
    console: Console,
    *,
    string: str, 
    fg: Optional[Tuple[int, int, int]] = color.white, 
    bg: Optional[Tuple[int, int, int]] = None
) -> None:
    for i, ch in enumerate(string):
        console.print(x, y + i, ch, fg=fg, bg=bg)

def render_bar(
    x: int, y: int, 
    console: Console,
    *,
    current_value: int, maximum_value: int, total_size: int, horizontal: bool = False,
    string: str = "",
    color_empty: Optional[Tuple[int, int, int]] = color.hp_bar_empty,
    color_filled: Optional[Tuple[int, int, int]] = color.hp_bar_filled,
    color_text: Optional[Tuple[int, int, int]] = color.hp_bar_text,
) -> None:
    bar_size = int(float(current_value) / maximum_value * total_size)

    if horizontal:
        console.draw_rect(x=x, y=y, width=total_size, height=1, ch=1, bg=color_empty)
        if bar_size > 0:
            console.draw_rect(x=x, y=y, width=bar_size, height=1, ch=1, bg=color_filled)
        console.print(x=x+1, y=y, string=f"{string} {current_value} / {maximum_value}", fg=color_text)
    else:
        console.draw_rect(x=x, y=y, width=1, height=total_size, ch=1, bg=color_empty)
        if bar_size > 0:
            console.draw_rect(x=x, y=y, width=1, height=bar_size, ch=1, bg=color_filled)
        print_vertical(x, y, console, string=f"{string} {current_value}~{maximum_value}", fg=color_text)

def render_names_at_mouse_location(
    console: Console,
    x: int, y: int,
    engine: Engine,
) -> None:
    game_map_pos = engine.game_map.pos_from_console_pos(engine.mouse_location, console, engine.camera)

    names = ""
    if engine.game_map.in_bounds(game_map_pos) and engine.game_map.visible[game_map_pos]:
        names = ", ".join(entity.name for entity in engine.game_map.entities if entity.pos == game_map_pos)

    console.print(x, y, names, fg=color.ui_subdued)

def render_health_bar(
    console: Console,
    current_hp: int,
    max_hp: int,
) -> None:
    render_bar(
        console.width - 2, 1, console,
        current_value = current_hp, maximum_value = max_hp, total_size = 20,
    )
    print_vertical(
        console.width - 2, 22, console,
        string = " HP ",
        fg = color.hp_bar_text, bg = color.hp_bar_filled
    )