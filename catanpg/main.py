import argparse
import logging
import random
import sys
from enum import Enum, IntEnum, auto
from typing import Any, Optional, Type

from catanpg.base.board import BaseBoard
from catanpg.base.board_image import BaseBoardImage
from catanpg.tab.board import FishermenOfCatanBoard
from catanpg.tab.board_image import FishermenOfCatanBoardImage


class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class Board(Enum):
    BASE = auto()
    FOC = auto()


class EnumAction(argparse.Action):
    """`argparse` action for handling Enums."""

    def __init__(self, type: Optional[Type] = None, **kwargs: Any):
        if type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(type, Enum):
            raise TypeError("type must be an Enum when using EnumAction")
        kwargs.setdefault("choices", tuple(e.name for e in type))
        super().__init__(**kwargs)
        self._enum = type

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Enum,
        option_string: Optional[str] = None
    ) -> None:
        value = self._enum[values]
        setattr(namespace, self.dest, value)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'board',
        type=Board,
        action=EnumAction,
        help="Set the type of board to generate."
    )
    parser.add_argument(
        '--ordered',
        action='store_true',
        dest='ordered',
        default=False,
        help="Place resource numbers as described in the Catan rulebook instead of randomly."
    )
    parser.add_argument(
        '--log',
        type=LogLevel,
        action=EnumAction,
        dest='log_level',
        default=LogLevel.WARNING,
        help=f"Set the log level (default is {LogLevel.WARNING})."
    )
    parser.add_argument(
        '--seed',
        type=int,
        action='store',
        dest='seed',
        default=None,
        help="Set the seed for the random generator (default is no fixed seed)."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    logging.basicConfig(level=args.log_level)
    seed = random.randrange(sys.maxsize) if args.seed is None else args.seed
    random.seed(seed)
    logging.info(f":random-seed {seed}")
    match args.board:
        case Board.BASE:
            board_cls, img_cls = BaseBoard, BaseBoardImage
        case Board.FOC:
            board_cls, img_cls = FishermenOfCatanBoard, FishermenOfCatanBoardImage
    board = board_cls(ordered_numbers=args.ordered)
    image = img_cls(board)
    image.show()
