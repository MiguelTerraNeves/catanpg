from abc import ABC
from typing import Iterable, Iterator

from catanpg.base.hex_tile import HexTile, HexTileWithOrientation, SeaTile

# TODO: docstrings


class TileSequence(ABC):

    def __init__(self, tiles: Iterable[HexTile]):
        self.tiles = list(tiles)

    def __len__(self) -> int:
        return len(self.tiles)

    def __iter__(self) -> Iterator[HexTile]:
        return iter(self.tiles)

    def rotate(self, nsteps: int) -> None:
        for tile in self.tiles:
            if isinstance(tile, HexTileWithOrientation):
                tile.rotate(nsteps)

    def rotate_clockwise(self) -> None:
        self.rotate(1)

    def rotate_counter_clockwise(self) -> None:
        self.rotate(-1)


class SeaBorderTile(TileSequence):

    def __init__(self) -> None:
        super().__init__([SeaTile() for _ in range(3)])
