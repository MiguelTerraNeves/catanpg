"""Hexagonal tiles for the base Catan board."""
from abc import ABC
from typing import Any

from hex_grid import Direction, rotate_direction

# TODO(mtn): docstrings


class HexTile(ABC):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


class NullHexTile(HexTile):
    pass


class DesertTile(HexTile):
    pass


class SeaTile(HexTile):
    pass


class NumberedHexTile(HexTile, ABC):

    def __init__(self, number: int, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.number = number


class ForestTile(NumberedHexTile):
    pass


class HillsTile(NumberedHexTile):
    pass


class PastureTile(NumberedHexTile):
    pass


class MountainsTile(NumberedHexTile):
    pass


class FieldsTile(NumberedHexTile):
    pass


class HexTileWithOrientation(HexTile, ABC):

    def __init__(self, direction: Direction, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.orientation = direction

    def rotate(self, nsteps: int) -> None:
        self.orientation = rotate_direction(self.orientation, nsteps)

    def rotate_clockwise(self) -> None:
        self.rotate(1)

    def rotate_counter_clockwise(self) -> None:
        self.rotate(-1)


class HarborTile(HexTileWithOrientation, SeaTile, ABC):
    pass


class ThreeOneHarborTile(HarborTile):
    pass


class WoolHarborTile(HarborTile):
    pass


class LumberHarborTile(HarborTile):
    pass


class OreHarborTile(HarborTile):
    pass


class GrainHarborTile(HarborTile):
    pass


class BrickHarborTile(HarborTile):
    pass
