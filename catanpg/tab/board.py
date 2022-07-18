import itertools as it
import random
from typing import Dict, List, Set, Tuple, Type

from catanpg.base.board import BaseBoard
from catanpg.base.hex_tile import DesertTile, HexTile, NumberOrNumbers
from catanpg.base.tile_sequence import SeaBorderTile
from catanpg.hex_grid import Direction, corner_at_distance, index_radius
from catanpg.tab.hex_tile import LAKE_NUMBERS, SEA_FISH_TILE_CLSS, LakeTile


class FishermenOfCatanBoard(BaseBoard):

    @property
    def _tile_cls_to_amount(self) -> Dict[Type[HexTile], int]:
        tile_cls_to_amount = super()._tile_cls_to_amount
        del tile_cls_to_amount[DesertTile]
        return tile_cls_to_amount

    @property
    def _forbidden_number_adjacencies(self) -> List[Set[NumberOrNumbers]]:
        return [set([6, 8, LAKE_NUMBERS])]

    def _mk_border_tiles(self) -> Tuple[List[SeaBorderTile], List[SeaBorderTile]]:
        single_harbor_borders, double_harbor_borders = super()._mk_border_tiles()
        sea_fish_tiles = [fish_tile_cls() for fish_tile_cls in SEA_FISH_TILE_CLSS]
        random.shuffle(sea_fish_tiles)
        for border in single_harbor_borders:
            border.tiles[2] = sea_fish_tiles.pop()
        for border in double_harbor_borders:
            border.tiles[1] = sea_fish_tiles.pop()
        assert len(sea_fish_tiles) == 0
        return single_harbor_borders, double_harbor_borders

    def _shuffle_tiles(self, ordered_numbers: bool) -> None:
        # Lake cannot be placed next to the sea borders
        lake_pos = random.choice(list(it.chain(list(Direction), [None])))
        lake_x, lake_y = corner_at_distance(lake_pos, 1) if lake_pos else (0, 0)
        self.grid.set(lake_x, lake_y, LakeTile())
        super()._shuffle_tiles(ordered_numbers)

    def _is_valid_swap(self, x_repair: int, y_repair: int, x_swap: int, y_swap: int) -> bool:
        def _not_invalid_lake_swap(x_maybe_lake: int, y_maybe_lake: int, x_other: int, y_other: int) -> bool:
            return (
                not isinstance(self.grid.get(x_maybe_lake, y_maybe_lake), LakeTile) or
                index_radius(x_other, y_other) < 2
            )
        return (
            super()._is_valid_swap(x_repair, y_repair, x_swap, y_swap) and
            _not_invalid_lake_swap(x_repair, y_repair, x_swap, y_swap) and
            _not_invalid_lake_swap(x_swap, y_swap, x_repair, y_repair)
        )
