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
        cpu_threads: int = 0,
        apu_threads: int = 0,
        data_storage: int = 0,
        max_shield: int = 0,
        shield_threshold: float = 0.0,
    ) -> None:
        self.max_hp = max_hp
        self.defence = defence
        self.power = power
        self.luck = luck
        self.cpu_threads = cpu_threads
        self.apu_threads = apu_threads
        self.data_storage = data_storage
        self.max_shield = max_shield
        self.shield_threshold = shield_threshold