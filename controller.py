from stone import ReversiStone
from model import ReversiModel


class ReversiController:

    def __init__(self):
        """
        初期化
        """
        self.__model = ReversiModel()
        self.__previous_board = self.__model.board.copy()


    def put(self, x: int, y: int):
        """
        (x, y)にコマを置く
        """
        self.__previous_board = self.__model.board.copy()

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
    def previous_board_str(self):
        """
        一手前の盤面を返す
        盤面には[x][y]でアクセスする
        """
        previous_board_str = [stone_kind.name if stone_kind != ReversiStone.CANDIDATE else 'EMPTY' for stone_kind in self.__previous_board]
        bd = [previous_board_str[10 * i + 1:10 * i + 9] for i in range(1, 9)]
        return tuple(zip(*bd))
    

    @property
    def xy_put(self):
        """
        コマを置いた座標を返す
        """
        y = int(self.__model.i_put / 10)
        x = int(self.__model.i_put -10*y)
        return [x-1, y-1]
    

    @property
    def xy_flips(self):
        """
        ひっくり返すコマらの座標を返す
        """
        xy_flips = []
        for i_flip in self.__model.i_flips:
            y = int(i_flip / 10)
            x = int(i_flip -10*y)
            xy_flips.append([x -1,y -1])
        return xy_flips
    

    @property
    def xy_candidates(self):
        """
        候補のコマらの座標を返す
        """
        xy_candidates = []
        for i_candidate in self.__model.i_candidates:
            y = int(i_candidate / 10)
            x = int(i_candidate -10*y)
            xy_candidates.append([x -1,y -1])
        return xy_candidates      
    

    @property
    def turn(self) -> ReversiStone:
        """
        現在のターンを ReversiStone で返す
        """
        return self.__model.turn
    

    @property
    def turn_str(self) -> str:
        """
        現在のターンを str で返す
        """
        return self.__model.turn.name


    @property
    def black_stone_count(self):
        """
        現在の黒石の数
        """
        return self.__model.board.count(ReversiStone.BLACK)
    
    
    @property
    def white_stone_count(self):
        """
        現在の白石の数
        """
        return self.__model.board.count(ReversiStone.WHITE)