from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Equipable (BaseComponent):
    def __init__(
        self,
        max_hp: int = 0,
        defence: int = 0,
        power: int = 0,
        luck: int = 0,
    ) -> None:
        self.max_hp = max_hp
        self.defence = defence
        self.power = power
        self.luck = luck
