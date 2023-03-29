from stone import ReversiStone
from model import ReversiModel


class ReversiController:

    def __init__(self):
        """
        初期化
        """
        self.__model = ReversiModel()


    def put(self, x: int, y: int):
        """
        (x, y)にコマを置く
        """
        x += 1
        y += 1
        is_put = self.__model.put(10 * y + x)
        return is_put
                

    @property
    def board_str(self):
        """
        盤面を返す
        盤面には[x][y]でアクセスする
        """
        board_str = [stone_kind.name for stone_kind in self.__model.board]
        bd = [board_str[10 * i + 1:10 * i + 9] for i in range(1, 9)]
        return tuple(zip(*bd))
    

    @property
    def turn(self) -> ReversiStone:
        return self.__model.turn
    

    @property
    def turn_str(self) -> str:
        return self.__model.turn.name