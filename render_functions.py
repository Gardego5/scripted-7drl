from __future__ import annotations

from typing import Tuple, Optional, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console

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
    current_value: int, maximum_value: int, total_size: int, horizontal: bool = True,
    color_empty: Optional[Tuple[int, int, int]] = color.hp_bar_empty,
    color_filled: Optional[Tuple[int, int, int]] = color.hp_bar_filled,
    color_text: Optional[Tuple[int, int, int]] = color.hp_bar_text,
) -> None:
    bar_size = int(float(current_value) / maximum_value * total_size)

    if horizontal:
        console.draw_rect(x=x, y=y, width=total_size, height=1, ch=1, bg=color_empty)
        if bar_size > 0:
            console.draw_rect(x=x, y=y, width=bar_size, height=1, ch=1, bg=color_filled)
        console.print(x=x+1, y=y, string=f" {current_value} / {maximum_value}", fg=color_text)
    else:
        console.draw_rect(x=x, y=y, width=1, height=total_size, ch=1, bg=color_empty)
        if bar_size > 0:
            console.draw_rect(x=x, y=y, width=1, height=bar_size, ch=1, bg=color_filled)
        print_vertical(x, y, console, string=f" {current_value}~{maximum_value}", fg=color_text)