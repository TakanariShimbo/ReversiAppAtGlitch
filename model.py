from stone import ReversiStone


"""
ToDo
コマをおける場所の提案
パスの実施
最後の点数計算
"""
class ReversiModel:

    def __init__(self):
        """
        初期化
        """
        # 全てEMPTYで盤面を作成
        self.__board = [ReversiStone.EMPTY] * 100

        # BLACKとWHITEのコマを配置
        self.__board[44] = ReversiStone.WHITE
        self.__board[45] = ReversiStone.BLACK
        self.__board[54] = ReversiStone.BLACK
        self.__board[55] = ReversiStone.WHITE

        # WALLを設定
        for i in range(10):
            self.__board[i] = ReversiStone.WALL
            self.__board[90 + i] = ReversiStone.WALL
            self.__board[10 * i] = ReversiStone.WALL
            self.__board[10 * i + 9] = ReversiStone.WALL


    @property
    def board(self):
        return self.__board
        

    def put(self, i_board: int, stone_kind: ReversiStone) -> bool:
        """
        盤面のi_boardに(BLACK or WHITE : stone_kind)のコマを置き、
        同じ色ではさんでいるマスをひっくり返す
        ひっくり返したらTrueを返す
        """
        i_turns = self.__flip_list(i_board, stone_kind)
        if not i_turns:
            return False
        
        self.__board[i_board] = stone_kind
        for i_turn in i_turns:
            self.__board[i_turn] = stone_kind
        return True

    
    def __flip_list(self, i_board: int, stone_kind: ReversiStone):
        """
        盤面のi_boardにtop(BLACK or WHITE)を置いたときに、
        ひっくり返されるマスのリストを返す
        """
        # 空マス以外なら空のリストを返す
        if self.__board[i_board] != ReversiStone.EMPTY:
            return []

        # 相手のコマ
        if stone_kind == ReversiStone.WHITE:
            enemy = ReversiStone.BLACK
        else:
            enemy = ReversiStone.WHITE

        # ひっくり返されるマスのリスト
        i_turns = []

        # 方向パラメータ
        UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
        RIGHT_UP, RIGHT_DOWN, LEFT_UP, LEFT_DOWN = RIGHT+UP, RIGHT+DOWN, LEFT+UP, LEFT+DOWN
        
        # 8方向を走査
        for v in (RIGHT, RIGHT_UP, UP, LEFT_UP, LEFT, LEFT_DOWN, DOWN, RIGHT_DOWN):
            # ひっくり返す候補
            temp = []

            # i_boardとの差
            delta = v

            # 敵のコマである限り、ひっくり返す候補に加え続ける
            while self.__board[i_board + delta] == enemy:
                temp.append(i_board + delta)
                delta += v
            
            # 敵のコマのあとが自分のコマなら候補を確定する
            if self.__board[i_board + delta] == stone_kind:
                i_turns += temp

        return i_turns