from __future__ import annotations

from typing import Optional
import random

import calculator


class Modifier:
    max_hp: int = 0
    defence: int = 0
    power: int = 0
    luck: int = 0
    cpu_threads: int = 0
    apu_threads: int = 0
    data_storage: int = 0
    max_shield: int = 0
    shield_threshold: float = 0

    whitelist: Set = set({})
    blacklist: Set = set({})

    name: str = "<Unnamed Modifier>"

    def __init__(
        self,
        level: int,
    ) -> None:
        self.level = level

class Intelligent (Modifier):
    whitelist = {"cpu"}
    name = "Intelligent"
    @property
    def luck(self) -> int:
        return max(random.randint(1, 3) * self.level + random.randint(-4, 1), 0) if random.random() < calculator.clamped_scale(self.level, min=0.25, max=0.7) else 0
    @property
    def cpu_threads(self) -> int:
        return 2 + self.level + (4 if random.random() < calculator.clamped_scale(self.level, min=0, max=0.5) else 0)
    @property
    def data_storage(self) -> int:
        return 2 * self.level if calculator.clamped_scale(self.level) else 2

class Planning (Modifier):
    whitelist = {"apu"}
    name = "Planning"
    @property
    def defence(self) -> int:
        return (5 if random.random() < calculator.clamped_scale(self.level, min=0.3, max=0.6) else 2) + self.level
    @property
    def apu_threads(self) -> int:
        return 2 + self.level + (4 if random.random() < calculator.clamped_scale(self.level, min=0, max=0.5) else 0)
    @property
    def data_storage(self) -> int:
        return 2 * self.level if calculator.clamped_scale(self.level) else 2

class Hard (Modifier):
    name = "Hard"
    @property
    def max_hp(self) -> int:
        return 10 + random.randint(4, 7) * self.level
    @property
    def defence(self) -> int:
        return 2 + self.level

class Reinforcing (Modifier):
    name = "Reinforcing"
    @property
    def defence(self) -> int:
        return 4 + self.level // 2
    @property
    def max_shield(self) -> int:
        return 15 + 10 * self.level

class Rash (Modifier):
    name = "Rash"
    @property
    def defence(self) -> int:
        return -2
    @property
    def power(self) -> int:
        return 6 + random.randint(0, 2) * self.level

class Lucky (Modifier):
    name = "Lucky"
    @property
    def luck(self) -> int:
        return 8 + max(0, self.level * 2 - 4)

class Cacheing (Modifier):
    name = "Cacheing"
    @property
    def data_storage(self) -> int:
        return 2 + self.level // 3
    @property
    def shield_threshold(self) -> float:
        return 0.08 + 0.05 * self.level

class Squinting (Modifier):
    whitelist = {"gpu"}
    name = "Squinting"
    @property
    def view_distance(self) -> int:
        return 2 + int(random.random() * calculator.clamped_scale(level, min = 2, max = 10))

class Discerning (Modifier):
    whitelist = {"d"}
    name = "Discerning"
    @property
    def view_distance(self) -> int:
        return 1 + self.level // 2 + max(0, self.level - 4)
    @property
    def data_storage(self) -> int:
        return -max(0, self.level - 4)

distribution = [
    (Intelligent, 10),
    (Planning, 10),
    (Hard, 20),
    (Reinforcing, 10),
    (Rash, 10),
    (Lucky, 4),
    (Cacheing, 20),
    (Squinting, 10),
    (Discerning, 1),
]