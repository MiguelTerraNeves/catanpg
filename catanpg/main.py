import argparse
import logging
from enum import Enum, IntEnum
from typing import Any, Optional, Type

from catanpg.base.board import BaseBoard
from catanpg.base.board_image import BaseBoardImage


class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


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
        '--log',
        type=LogLevel,
        action=EnumAction,
        dest='log_level',
        default=LogLevel.WARNING,
        help=f"Set the log level (default is {LogLevel.WARNING})"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    logging.basicConfig(level=args.log_level)
    board = BaseBoard()
    image = BaseBoardImage(board)
    image.show()
