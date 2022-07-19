"""Hexagonal grid data structure and utilities."""
import itertools as it
import operator
from enum import IntEnum
from typing import Any, Iterator, Optional, Tuple, cast

# TODO: docstrings


class Direction(IntEnum):
    EAST = 0
    SOUTHEAST = 1
    SOUTHWEST = 2
    WEST = 3
    NORTHWEST = 4
    NORTHEAST = 5


_DIRECTION_TO_VECTOR = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
_DIRECTION_TO_ANGLE = [0, 300, 240, 180, 120, 60]


def direction_to_angle(direction: Direction) -> float:
    return _DIRECTION_TO_ANGLE[direction]


def move_from_hex(x: int, y: int, direction: Direction, nsteps: int) -> Tuple[int, int]:
    return cast(
        Tuple[int, int],
        tuple(map(operator.add, (x, y), tuple(map(operator.mul, _DIRECTION_TO_VECTOR[direction], (nsteps, nsteps)))))
    )


def step_from_hex(x: int, y: int, direction: Direction) -> Tuple[int, int]:
    return move_from_hex(x, y, direction, 1)


def corner_at_distance(direction: Direction, radius: int) -> Tuple[int, int]:
    return move_from_hex(0, 0, direction, radius)


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    dist = (abs(x1 - x2) + abs(x1 + y1 - x2 - y2) + abs(y1 - y2)) / 2
    assert dist.is_integer()
    return int(dist)


def index_radius(x: int, y: int) -> int:
    return distance(x, y, 0, 0)


def rotate_direction(direction: Direction, nsteps: int) -> Direction:
    return Direction((direction + nsteps) % 6)


def next_clockwise_direction(direction: Direction) -> Direction:
    return rotate_direction(direction, 1)


def next_counter_clockwise_direction(direction: Direction) -> Direction:
    return rotate_direction(direction, -1)


def symmetric_direction(direction: Direction) -> Direction:
    return Direction((direction + 3) % 6)


def symmetric_index(x: int, y: int) -> Tuple[int, int]:
    return -x, -y


def ordered_ring_indexes(start_corner: Direction, radius: int) -> Iterator[Tuple[int, int]]:
    if radius == 0:
        yield 0, 0
    else:
        x, y = corner_at_distance(start_corner, radius)
        for i in range(6):
            for _ in range(radius):
                yield x, y
                x, y = step_from_hex(x, y, Direction((i+2+start_corner) % 6))


def spiral_ordered_indexes(start_corner: Direction, radius: int) -> Iterator[Tuple[int, int]]:
    for i in reversed(range(radius+1)):
        yield from ordered_ring_indexes(start_corner, i)


def neighbors(x: int, y: int) -> Iterator[Tuple[int, int]]:
    for direction in Direction:
        yield step_from_hex(x, y, direction)


# TODO: parameterizable typing instead of Any
# TODO: rectangular hex grids instead of just circular
class HexGrid:

    def __init__(self, radius: int):
        self._radius = radius
        self._grid = []
        for _ in range(radius*2+1):
            self._grid.append(list(it.repeat(None, radius*2 + 1)))

    @property
    def radius(self) -> int:
        return self._radius

    def _within_grid(self, x: int, y: int) -> bool:
        return abs(x) <= self.radius and abs(y) <= self.radius and abs(-x-y) <= self.radius

    def _ensure_within_grid(self, x: int, y: int) -> None:
        if not self._within_grid(x, y):
            raise ValueError(f"({x}, {y}) is outside hex grid of radius {self.radius}")

    def set(self, x: int, y: int, el: Any) -> None:
        self._ensure_within_grid(x, y)
        self._grid[x + self.radius][y + self.radius] = el

    def get(self, x: int, y: int) -> Any:
        self._ensure_within_grid(x, y)
        return self._grid[x + self.radius][y + self.radius]

    def is_free(self, x: int, y: int) -> bool:
        self._ensure_within_grid(x, y)
        return self._grid[x + self.radius][y + self.radius] is None

    def furthest_corner(self, direction: Direction) -> Tuple[int, int]:
        return corner_at_distance(direction, self.radius)

    def ordered_ring_hexes(self, start_corner: Direction, radius: int) -> Iterator[Any]:
        for x, y in ordered_ring_indexes(start_corner, radius):
            yield self.get(x, y)

    def spiral_ordered_hexes(self, start_corner: Direction, radius: Optional[int] = None) -> Iterator[Any]:
        if radius is not None and radius > self.radius:
            raise ValueError(f"Radius cannot be larger than {self.radius} (got {radius} instead)")
        for x, y in spiral_ordered_indexes(start_corner, radius if radius is not None else self.radius):
            yield self.get(x, y)

    def neighbor_indexes(self, x: int, y: int) -> Iterator[Tuple[int, int]]:
        for x_n, y_n in neighbors(x, y):
            if self._within_grid(x_n, y_n):
                yield x_n, y_n

    def neighbors(self, x: int, y: int) -> Iterator[Any]:
        for x_n, y_n in self.neighbor_indexes(x, y):
            yield self.get(x_n, y_n)
