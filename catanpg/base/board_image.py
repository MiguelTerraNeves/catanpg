import math
from typing import Tuple, Union

from PIL import Image, ImageDraw, ImageFont

from catanpg.base.board import BaseBoard
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
    OreHarborTile,
    PastureTile,
    SeaTile,
    ThreeOneHarborTile,
    WoolHarborTile,
)
from catanpg.hex_grid import Direction, direction_to_angle, spiral_ordered_indexes

_Color = Union[str, Tuple[int, int, int, int]]

_HEX_EDGE_LENGTH = 40
_LINE_SEGMENT_THICKNESS = 6
_PORT_CIRCLE_RADIUS = 12
_PORT_FONT_SIZE = 17
_PORT_COLOR = (255, 223, 128, 0)


def _degrees_to_radians(degrees: float) -> float:
    return math.pi/180 * degrees


def _pixel_at_distance(x: int, y: int, distance: float, angle_degrees: float) -> Tuple[int, int]:
    angle_rad = _degrees_to_radians(angle_degrees)
    return int(x + distance*math.cos(angle_rad)), int(y - distance*math.sin(angle_rad))


def _axial_to_pixel(x: int, y: int, radius: int) -> Tuple[int, int]:
    return 50 + 100*radius + 36*y + 72*x, 100*(2*radius+1) - 50 - 100*radius + 62*y


def _draw_text(draw: ImageDraw, center_x: int, center_y: int, text: str, size: int) -> None:
    text_font = ImageFont.truetype("arial", size)
    w, h = draw.textsize(text, font=text_font)
    draw.text((center_x-w/2, center_y-h/2), text, fill='black', font=text_font)


def _draw_circle(draw: ImageDraw, center_x: int, center_y: int, radius: int, fill: _Color) -> None:
    draw.ellipse(((center_x-radius, center_y-radius), (center_x+radius, center_y+radius)), outline='black', fill=fill)


def _draw_hexagon(draw: ImageDraw, center_x: int, center_y: int, fill: _Color) -> None:
    x: float = center_x
    y: float = center_y-_HEX_EDGE_LENGTH
    hexagon = []
    for angle in range(0, 360, 60):
        x += math.cos(math.radians(angle+30)) * _HEX_EDGE_LENGTH
        y += math.sin(math.radians(angle+30)) * _HEX_EDGE_LENGTH
        hexagon.append((x, y))
    draw.polygon(hexagon, outline='black', fill=fill)


def _draw_number_circle(draw: ImageDraw, center_x: int, center_y: int, number: int) -> None:
    _draw_circle(draw, center_x, center_y, 20, (255, 255, 204, 0))
    _draw_text(draw, center_x, center_y, str(number), 30)


def _draw_to_corner_line_segment(draw: ImageDraw, center_x: int, center_y: int, angle: float, fill: _Color) -> None:
    line_edge_x, line_edge_y = _pixel_at_distance(center_x, center_y, _HEX_EDGE_LENGTH, angle)
    draw.line((center_x, center_y, line_edge_x, line_edge_y), fill, _LINE_SEGMENT_THICKNESS)


def _get_hex_tile_color(tile: HexTile) -> _Color:
    match tile:
        case DesertTile():
            return (255, 223, 128, 0)
        case SeaTile():
            return (0, 46, 184, 0)
        case ForestTile():
            return (0, 128, 0, 0)
        case HillsTile():
            return (204, 102, 0, 0)
        case PastureTile():
            return (36, 255, 36, 0)
        case MountainsTile():
            return (0, 214, 214, 0)
        case FieldsTile():
            return (240, 240, 0, 0)
        case _:
            raise ValueError(f"Unknown tile type {tile.__class__.__name__}")


def _draw_hex_tile(draw: ImageDraw, center_x: int, center_y: int, tile: HexTile) -> None:
    _draw_hexagon(draw, center_x, center_y, _get_hex_tile_color(tile))
    if isinstance(tile, NumberedHexTile):
        _draw_number_circle(draw, center_x, center_y, tile.number)


def _get_port_label(tile: HarborTile) -> str:
    match tile:
        case ThreeOneHarborTile():
            return "3"
        case WoolHarborTile():
            return "W"
        case LumberHarborTile():
            return "L"
        case OreHarborTile():
            return "O"
        case GrainHarborTile():
            return "G"
        case BrickHarborTile():
            return "B"
        case _:
            raise ValueError(f"Unknown harbor type {tile.__class__.__name__}")


def _draw_port(draw: ImageDraw, center_x: int, center_y: int, tile: HarborTile) -> None:
    _draw_to_corner_line_segment(draw, center_x, center_y, direction_to_angle(tile.orientation)+30, _PORT_COLOR)
    _draw_to_corner_line_segment(draw, center_x, center_y, direction_to_angle(tile.orientation)-30, _PORT_COLOR)
    _draw_circle(draw, center_x, center_y, _PORT_CIRCLE_RADIUS, _PORT_COLOR)
    _draw_text(draw, center_x, center_y, _get_port_label(tile), _PORT_FONT_SIZE)


class BaseBoardImage:

    def __init__(self, board: BaseBoard) -> None:
        self.board = board

    def show(self) -> None:
        radius = self.board.grid.radius
        image = Image.new('RGB', (100*(2*radius+1), 100*(2*radius+1)), 'white')
        draw = ImageDraw.Draw(image)
        for x, y in spiral_ordered_indexes(Direction.EAST, radius):
            hex_tile = self.board.grid.get(x, y)
            assert isinstance(hex_tile, HexTile)
            pixel = _axial_to_pixel(x, y, radius)
            _draw_hex_tile(draw, *pixel, hex_tile)
            if isinstance(hex_tile, HarborTile):
                _draw_port(draw, *pixel, hex_tile)
        image.show()
