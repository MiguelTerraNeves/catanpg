from catanpg.base.board import BaseBoard
from catanpg.base.board_image import BaseBoardImage

if __name__ == "__main__":
    board = BaseBoard()
    image = BaseBoardImage(board)
    image.show()
