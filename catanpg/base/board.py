import itertools as it
import logging
import random
from copy import deepcopy
from typing import Dict, List, Optional, Sequence, Set, Tuple, Type

from catanpg.base.hex_tile import (
    BrickHarborTile,
    DesertTile,
    FieldsTile,
    ForestTile,
    GrainHarborTile,
    HarborTile,
    HexTile,
    HillsTile,
    LumberHarborTile,
    MountainsTile,
    NumberedHexTile,
    NumberOrNumbers,
    OreHarborTile,
    PastureTile,
    SeaTile,
    ThreeOneHarborTile,
    WoolHarborTile,
)
from catanpg.base.tile_sequence import SeaBorderTile
from catanpg.hex_grid import (
    Direction,
    HexGrid,
    corner_at_distance,
    move_from_hex,
    next_clockwise_direction,
    spiral_ordered_indexes,
)

# TODO: docstrings

_ORDERED_NUMBERS = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]

_RESTART_THRESHOLD = 10


def _roulette_wheel_selection(weights: Sequence[int]) -> int:
    assert any(w > 0 for w in weights) and all(w >= 0 for w in weights)
    weight_sample = random.randint(1, sum(weights))
    weight_acc = weights[0]
    idx = 0
    while weight_acc < weight_sample:
        idx += 1
        weight_acc += weights[idx]
    return idx


def _mk_harbor_boder(tile_overrides: Sequence[Optional[SeaTile]] = (None, None, None)) -> SeaBorderTile:
    if len(tile_overrides) != 3:
        raise ValueError("The custom tile overrides for a sea border must be a sequence of length 3")
    border = SeaBorderTile()
    for i, tile in enumerate(tile_overrides):
        if tile:
            border.tiles[i] = tile
    return border


def _mk_single_harbor_border(harbor_class: Type[HarborTile]) -> SeaBorderTile:
    return _mk_harbor_boder((None, harbor_class(Direction.SOUTHEAST), None))


def _mk_double_harbor_border(harbor1_class: Type[HarborTile], harbor2_class: Type[HarborTile]) -> SeaBorderTile:
    return _mk_harbor_boder((harbor1_class(Direction.SOUTHEAST), None, harbor2_class(Direction.SOUTHWEST)))


class BaseBoard:

    def __init__(self, ordered_numbers: bool = False) -> None:
        done = False
        while not done:
            self.grid = HexGrid(3)
            self._shuffle_borders()
            self._shuffle_tiles(ordered_numbers)
            done = self._fix_violations()

    @property
    def _tile_cls_to_amount(self) -> Dict[Type[HexTile], int]:
        return {
            ForestTile: 4,
            PastureTile: 4,
            FieldsTile: 4,
            HillsTile: 3,
            MountainsTile: 3,
            DesertTile: 1
        }

    @property
    def _forbidden_number_adjacencies(self) -> List[Set[NumberOrNumbers]]:
        return [set((6, 8))]

    def _mk_border_tiles(self) -> Tuple[List[SeaBorderTile], List[SeaBorderTile]]:
        harbor_class_pairs = (
            (ThreeOneHarborTile, WoolHarborTile),
            (ThreeOneHarborTile, BrickHarborTile),
            (ThreeOneHarborTile, GrainHarborTile)
        )
        return (
            list(map(_mk_single_harbor_border, (LumberHarborTile, ThreeOneHarborTile, OreHarborTile))),
            list(it.starmap(_mk_double_harbor_border, harbor_class_pairs))
        )

    def _shuffle_borders(self) -> None:
        single_harbor_borders, double_harbor_borders = self._mk_border_tiles()
        assert len(single_harbor_borders) == len(double_harbor_borders)
        random.shuffle(single_harbor_borders)
        random.shuffle(double_harbor_borders)
        corner = Direction.NORTHWEST
        orientation = Direction.EAST
        for i, border in enumerate(it.chain(*zip(single_harbor_borders, double_harbor_borders))):
            border.rotate(i)
            for i, tile in enumerate(border):
                self.grid.set(*move_from_hex(*corner_at_distance(corner, 3), orientation, i), tile)
            corner = next_clockwise_direction(corner)
            orientation = next_clockwise_direction(orientation)

    def _shuffle_tiles(self, ordered_numbers: bool) -> None:
        numbers = list(reversed(_ORDERED_NUMBERS))
        if not ordered_numbers:
            random.shuffle(numbers)
        tile_clss = [tile_cls for tile_cls, amount in self._tile_cls_to_amount.items() for _ in range(amount)]
        random.shuffle(tile_clss)
        for x, y in spiral_ordered_indexes(Direction.EAST, 2):
            if self.grid.is_free(x, y):
                tile_cls = tile_clss.pop()
                tile = tile_cls(numbers.pop()) if issubclass(tile_cls, NumberedHexTile) else tile_cls()
                self.grid.set(x, y, tile)
        assert len(numbers) == len(tile_clss) == 0

    def _tile_violation(self, grid: HexGrid, x: int, y: int) -> int:
        tile = grid.get(x, y)
        if not isinstance(tile, NumberedHexTile):
            return 0
        return sum(
            1
            for constraint in self._forbidden_number_adjacencies
            if tile.number in constraint
            for near_tile in grid.neighbors(x, y)
            if isinstance(near_tile, NumberedHexTile) and near_tile.number in constraint
        )

    def _grid_violation(self, grid: HexGrid) -> int:
        return sum(self._tile_violation(grid, x, y) for x, y in spiral_ordered_indexes(Direction.EAST, 2))

    def _select_violating_index(self) -> Tuple[int, int]:
        indexes = list(spiral_ordered_indexes(Direction.EAST, 2))
        return indexes[_roulette_wheel_selection([self._tile_violation(self.grid, x, y) for x, y in indexes])]

    def _is_valid_swap(self, x_repair: int, y_repair: int, x_swap: int, y_swap: int) -> bool:
        return True

    def _fix_violations(self) -> bool:
        logging.info(f":initial-violation {self._grid_violation(self.grid)}")
        fix_iter = 0
        while self._grid_violation(self.grid) > 0 and fix_iter < _RESTART_THRESHOLD:
            idx_repair = self._select_violating_index()
            tile_repair = self.grid.get(*idx_repair)
            assert isinstance(tile_repair, NumberedHexTile)
            swapped_grids = []
            valid_swap_it = iter(
                idx for idx in spiral_ordered_indexes(Direction.EAST, 2)
                if idx_repair != idx and self._is_valid_swap(*idx_repair, *idx)
            )
            for idx_swap in valid_swap_it:
                tile_swap = self.grid.get(*idx_swap)
                if isinstance(tile_swap, NumberedHexTile):
                    new_grid = deepcopy(self.grid)
                    new_grid.set(*idx_repair, tile_repair.__class__(tile_swap.number))
                    new_grid.set(*idx_swap, tile_swap.__class__(tile_repair.number))
                    swapped_grids.append(new_grid)
            grid_viols = list(map(self._grid_violation, swapped_grids))
            min_viol = min(grid_viols)
            min_viol_grids = [grid for grid, viol in zip(swapped_grids, grid_viols) if viol == min_viol]
            self.grid = random.choice(min_viol_grids)
            fix_iter += 1
            logging.info(f":fix-iteration {fix_iter} :new-violation {min_viol}")
        return fix_iter < _RESTART_THRESHOLD
