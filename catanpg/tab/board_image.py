from catanpg.base.board_image import BaseBoardImage, Color
from catanpg.base.hex_tile import HexTile, NumberOrNumbers
from catanpg.tab.hex_tile import FishTile


class FishermenOfCatanBoardImage(BaseBoardImage):

    def _get_hex_tile_color(self, tile: HexTile) -> Color:
        if isinstance(tile, FishTile):
            return (0, 138, 184, 0)
        return super()._get_hex_tile_color(tile)

    def _draw_number_circle(self, center_x: int, center_y: int, number: NumberOrNumbers) -> None:
        if not isinstance(number, int) and len(number) == 4:
            center = [center_x-14, center_y-14]
            self._draw_empty_number_circle(*center, 12)
            self._draw_text(*center, str(number[0]), 18)
            center[0] = center_x+14
            self._draw_empty_number_circle(*center, 12)
            self._draw_text(*center, str(number[1]), 18)
            center[1] = center_y+14
            self._draw_empty_number_circle(*center, 12)
            self._draw_text(*center, str(number[3]), 18)
            center[0] = center_x-14
            self._draw_empty_number_circle(*center, 12)
            self._draw_text(*center, str(number[2]), 18)
        else:
            super()._draw_number_circle(center_x, center_y, number)
