"""Hexagonal tiles for the Traders and Barbarians boards."""
from abc import ABC
from typing import Any

from catanpg.base.hex_tile import NumberedHexTile, SeaTile

LAKE_NUMBERS = (11, 12, 2, 3)


class FishTile(NumberedHexTile, ABC):
    pass


class SeaFishTile(SeaTile, FishTile, ABC):
    pass


class Sea4FishTile(SeaFishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(4, *args, **kwargs)


class Sea5FishTile(SeaFishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(5, *args, **kwargs)


class Sea6FishTile(SeaFishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(6, *args, **kwargs)


class Sea8FishTile(SeaFishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(8, *args, **kwargs)


class Sea9FishTile(SeaFishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(9, *args, **kwargs)


class Sea10FishTile(SeaFishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(10, *args, **kwargs)


SEA_FISH_TILE_CLSS = (Sea4FishTile, Sea5FishTile, Sea6FishTile, Sea8FishTile, Sea9FishTile, Sea10FishTile)


class LakeTile(FishTile):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(LAKE_NUMBERS, *args, **kwargs)
