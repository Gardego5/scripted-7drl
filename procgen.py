from typing import Tuple, Callable

import numpy as np
import random
import queue

from tcod import heightmap_add

from game_map import GameMap
import tile_types


class Room:
    def __init__(
        self,
        x: int, y: int,
        width: int, height: int, 
        palette = (tile_types.wall, tile_types.floor)
    ) -> None:
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x + width, y + height
        self.width, self.height = width, height
        self.palette = palette
        self.clear()
    
    @property
    def center(self) -> Tuple[int, int]:
        return int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2)

    @property  # Defines the slice where this room should exist on the map.
    def bounds(self) -> Tuple[slice, slice]:
        return slice(self.x1, self.x2), slice(self.y1, self.y2)

    def clear(self) -> None:
        self.tiles = np.full((self.width, self.height), fill_value=self.palette[0], order="F")

    def generate(self) -> None:
        raise NotImplementedError()

    def add_margin(self, margin: Tuple[int, int, int, int]=(1, 0, 0, 1)) -> None:
        self.tiles[:, 0:margin[0]] = self.palette[0]
        self.tiles[-margin[1]:self.width, :] = self.palette[0]
        self.tiles[:, -margin[2]:self.height] = self.palette[0]
        self.tiles[0:margin[3], :] = self.palette[0]

class RectangularRoom (Room):
    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        palette=(tile_types.wall, tile_types.floor),
    ) -> None:
        super().__init__(x, y, width, height, palette)
        self.generate()

    def generate(self) -> None:
        self.tiles[0:self.width, 0:self.height] = self.palette[1]

class CrossRoom (Room):
    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        palette=(tile_types.wall, tile_types.floor),
    ) -> None:
        super().__init__(x, y, width, height, palette)
        self.generate()
    
    def generate(self) -> None:
        x_width, y_width = random.randint(1, self.width - 1), random.randint(1, self.height - 1)
        x_pos, y_pos = random.randint(0, self.width - x_width), random.randint(0, self.height - y_width)
        self.tiles[x_pos:x_pos + x_width, :] = self.palette[1]
        self.tiles[:, y_pos:y_pos + y_width] = self.palette[1]

class MarchingRoom (Room):
    _cardinals = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]

    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        palette=(tile_types.wall, tile_types.floor),
        dist: int = None, rotate: float = 0.3, 
    ) -> None:
        super().__init__(x, y, width, height, palette)
        if dist == None: dist = int(width * height * 0.8)
        self.generate(dist=dist, rotate=rotate)
    
    def generate(self, dist: int, rotate: float = 0.3) -> None:
        x_pos, y_pos, dir = int(self.width / 2), int(self.height / 2), random.randint(0, 3)
        i = 0
        while i < dist:
            if 0 <= x_pos + self._cardinals[dir][0] < self.width and 0 <= y_pos + self._cardinals[dir][1] < self.height:
                self.tiles[x_pos, y_pos] = self.palette[1]
                x_pos, y_pos = x_pos + self._cardinals[dir][0], y_pos + self._cardinals[dir][1]
                i += 1
            else:
                dir += random.choice([-1, 1])
                if dir > 3: dir = 0
                if dir < 0: dir = 3

            if random.random() < rotate:
                dir += random.choice([-1, 1])
                if dir > 3: dir = 0
                if dir < 0: dir = 3

class CellularRoom (Room):
    _smoothing_areas = {
        "r": [(-1, -1), ( 0, -1), ( 1, -1),
              (-1,  0),           ( 1,  0),
              (-1,  1), ( 0,  1), ( 1,  1)],
        "t": [          ( 0, -1),
              (-1,  0),           ( 1,  0),
                        ( 0,  1),         ],
        "x": [(-1, -1),           ( 1, -1),
                                 
              (-1,  1),           ( 1,  1)],
        "R": [(-2, -2), (-1, -2), ( 0, -2), ( 1, -2), ( 2, -2),
              (-2, -1), (-1, -1), ( 0, -1), ( 1, -1), ( 2, -1),
              (-2,  0), (-1,  0),           ( 1,  0), ( 2,  0),
              (-2,  1), (-1,  1), ( 0,  1), ( 1,  1), ( 2,  1),
              (-2,  2), (-1,  2), ( 0,  2), ( 1,  2), ( 2,  2),],
        "T": [                    ( 0, -2),                    
                        (-1, -1), ( 0, -1), ( 1, -1),          
              (-2,  0), (-1,  0),           ( 1,  0), ( 2,  0),
                        (-1,  1), ( 0,  1), ( 1,  1),          
                                  ( 0,  2),                    ],
        "X": [(-2, -2),                               ( 2, -2),
                        (-1, -1),           ( 1, -1),          
                                                                
                        (-1,  1),           ( 1,  1),          
              (-2,  2),                               ( 2,  2),],
        "+": [                    ( 0, -2),                    
                                  ( 0, -1),
              (-2,  0), (-1,  0),           ( 1,  0), ( 2,  0),
                                  ( 0,  1),
                                  ( 0,  2),                    ],
        "::": [(-2, -2),                               ( 2, -2),


              
              (-2,  2),                               ( 2,  2),],
    }

    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        palette=(tile_types.wall, tile_types.floor),
        smoothing: int = 2, smoothing_area: str = "T", threshold: float = 0.5, 
    ) -> None:
        super().__init__(x, y, width, height, palette)
        self.generate(smoothing=smoothing, smoothing_area=smoothing_area, threshold=threshold)
    
    def fill_raw(self) -> np.array:
        self.tiles_raw =  np.random.rand(self.width, self.height)

    def smooth_raw(self, smoothing_area: str = "r") -> None:
        new_tiles_raw = np.copy(self.tiles_raw)

        for y, row in enumerate(self.tiles_raw):
            for x, data in enumerate(row):
                total, considered = 0, 0
                considered_x, considered_y = 0, 0

                for point in self._smoothing_areas[smoothing_area]:
                    considered_x, considered_y = x + point[0], y + point[1]
                    try:
                        total += self.tiles_raw[considered_x, considered_y]
                        considered += 1
                    except IndexError:
                        pass
            
                new_tiles_raw[x, y] = total / considered
        
        self.tiles_raw = new_tiles_raw 

    def from_raw(self, f: Callable[[float], Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]]):
        for y, row in enumerate(self.tiles_raw):
            for x, data in enumerate(row):
                self.tiles[x, y] = f(data)

    def generate(
        self, 
        smoothing: int = 1, smoothing_area: str = "r", threshold: float = 0.5
    ) -> None:
        self.fill_raw()

        for i in range(smoothing):
            self.smooth_raw(smoothing_area)

        self.from_raw(lambda x: self.palette[1] if x < np.sort(self.tiles_raw, axis=None)[int(self.width * self.height * threshold)] else self.palette[0])

class FloodedCellsRoom (CellularRoom):
    @staticmethod
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def __init__(
        self, 
        x: int, y: int, width: int, height: int, 
        palette=(tile_types.wall, tile_types.floor), 
        smoothing: int = 2, smoothing_area: str = "T", threshold: float = 0.5,
        start: Tuple[int, int] = None, nearest_smoothing_area: str = "t",
    ) -> None:
        super(CellularRoom, self).__init__(x, y, width, height, palette)
        self.generate(
            smoothing=smoothing, smoothing_area=smoothing_area, threshold=threshold,
            start=start, nearest_smoothing_area=nearest_smoothing_area)

    def generate(
        self, 
        smoothing: int = 1, smoothing_area: str = "r", threshold: float = 0.5,
        start: Tuple[int, int] = None, nearest_smoothing_area: str = "t",
    ) -> None:
        if start == None: start = (int(self.width / 2), int(self.height / 2))

        self.fill_raw()

        for i in range(smoothing):
            self.smooth_raw(smoothing_area)
        
        start_value = self.tiles_raw[start[0], start[1]]
        SortedQueue = {start_value: start}  # A dictionary to hold all key sortable relative to their value

        for i in range(int(self.width * self.height * threshold)):
            considered_value = self.find_nearest([k for k, v in SortedQueue.items()], start_value)
            considered_loc = (SortedQueue[considered_value][0], SortedQueue[considered_value][1])
            SortedQueue.pop(considered_value)

            self.tiles_raw[considered_loc[0], considered_loc[1]] = 2

            for offset in self._smoothing_areas[nearest_smoothing_area]:
                offset_loc = (offset[0] + considered_loc[0], offset[1] + considered_loc[1])
                if 0 <= offset_loc[0] < self.width and 0 <= offset_loc[1] < self.height:
                    SortedQueue[self.tiles_raw[offset_loc[0], offset_loc[1]]] = offset_loc
        
        self.from_raw(lambda x: self.palette[1] if x == 2 else self.palette[0])


def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = MarchingRoom(0, 0, 20, 20, rotate=1)
    room_2 = MarchingRoom(25, 0, 20, 20, rotate=1)
    room_3 = MarchingRoom(50, 0, 20, 20, rotate=1)
    room_4 = MarchingRoom(0, 25, 20, 20, rotate=1)
    room_5 = MarchingRoom(25, 25, 20, 20, rotate=1)
    room_6 = MarchingRoom(50, 25, 20, 20, rotate=1)

    rooms = [room_1, room_2, room_3, room_4, room_5, room_6]

    for room in rooms:
        #room.add_margin((1, 1, 1, 1))
        dungeon.tiles[room.bounds] = room.tiles

    return dungeon