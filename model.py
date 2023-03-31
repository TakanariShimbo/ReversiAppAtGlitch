from stone import ReversiStone


"""
ToDo
最後の点数計算
"""
class ReversiModel:

    def __init__(self):
        """
        初期化
        """
        # 全てEMPTYで盤面を作成
        self.__board = [ReversiStone.EMPTY] * 100
        self.__turn = ReversiStone.BLACK
        self.__i_put = None
        self.__i_flips = []
        self.__i_candidates = []

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

        # 候補を探索
        current_stone_kind = self.__turn
        self.__search_candidates(current_stone_kind)


    @property
    def board(self):
        return self.__board
    
    @property
    def turn(self):
        return self.__turn
    
    @property
    def i_put(self):
        return self.__i_put
    
    @property
    def i_flips(self):
        return self.__i_flips
    
    @property
    def i_candidates(self):
        return self.__i_candidates

    def put(self, i_board: int) -> bool:
        """
        盤面のi_boardに(BLACK or WHITE : stone_kind)のコマを置き、
        同じ色ではさんでいるマスをひっくり返す
        1. ひっくり返したらTrue、返せなければFalseを返す
        2. 次のコマの種類を返す
        """
        # Early return
        if not self.__can_flip(i_board):
            return False
        
        # コマを置き、ひっくり返す
        current_stone_kind = self.__turn
        self.__flip_stones(i_board, current_stone_kind)

        # 次のコマを置ける候補を探す
        reverse_stone_kind = self.__get_reverse_stone_kind(self.__turn)
        is_find_candidate = self.__search_candidates(reverse_stone_kind)

        # 候補が見つかったので、次は反対の色のプレイヤーのターン
        if is_find_candidate:
            self.__turn = reverse_stone_kind
            return True
        
        # 候補が見つからなかったので、反対の色のターンはスキップされ、同じプレイヤーの候補を再検索する
        current_stone_kind = self.__get_reverse_stone_kind(reverse_stone_kind)
        is_find_candidate = self.__search_candidates(current_stone_kind)

        # 候補が見つかったので、次も自分のターン
        if is_find_candidate:
            self.__turn = current_stone_kind
            return True
        
        # どちらの色の候補も見つからなかったのでゲーム終了
        self.__turn = ReversiStone.EMPTY
        return True


    def __can_flip(self, i_board: int) -> bool:
        """
        盤面のi_boardにコマを置いたときひっくり返せるかどうか
        ひっくり返せるならTrue、返せなければFalseを返す
        """
        # 候補以外なら空のリストを返す
        if self.__board[i_board] != ReversiStone.CANDIDATE:
            return False
        
        return True
        
                
    def __flip_stones(self, i_board: int, put_stone_kind: ReversiStone) -> None:
        """
        盤面のi_boardにput_stone_kind(BLACK or WHITE)を置かれたとして、コマをひっくり返す
        ひっくり返されたらTrue、返されなければFalseを返す
        """

        # 相手のコマ
        enemy_stone_kind = self.__get_reverse_stone_kind(put_stone_kind)

        # ひっくり返されるマスのリスト
        i_flips = []

        # 方向パラメータ
        UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
        RIGHT_UP, RIGHT_DOWN, LEFT_UP, LEFT_DOWN = RIGHT+UP, RIGHT+DOWN, LEFT+UP, LEFT+DOWN
        
        # 8方向を走査
        for i_unit in (RIGHT, RIGHT_UP, UP, LEFT_UP, LEFT, LEFT_DOWN, DOWN, RIGHT_DOWN):
            # ひっくり返す候補
            i_flips_temp = []

            # 置いたコマの隣が敵のコマ出なければ次へ
            i_check = i_board + i_unit
            if self.__board[i_check] != enemy_stone_kind:
                continue

            # 敵のコマである限り、unit_vec方向に進み続ける
            while self.__board[i_check] == enemy_stone_kind:
                i_flips_temp.append(i_check)
                i_check += i_unit
            
            # 敵のコマのあとが自分のコマなら置けることが確定
            if self.__board[i_check] == put_stone_kind:
                i_flips += i_flips_temp

        # コマを置く、ひっくり返す
        self.__board[i_board] = put_stone_kind
        for i_flip in i_flips:
            self.__board[i_flip] = put_stone_kind
        self.__i_put = i_board
        self.__i_flips = i_flips

    def __get_reverse_stone_kind(self, stone_kind: ReversiStone) -> ReversiStone:
        """
        反対のコマの種類を取得
        """
        if stone_kind == ReversiStone.BLACK:
            return ReversiStone.WHITE
        else:
            return ReversiStone.BLACK
            

    def __search_candidates(self, next_stone_kind: ReversiStone) -> bool:
        """
        次のターンの人が置ける場所を置ける場所を探索する
        次のターンの人が置ける場所があればTrue、なければFalseを返す
        """
        # 現在の候補を空に
        for i, stone_kind in enumerate(self.__board.copy()):
            if stone_kind == ReversiStone.CANDIDATE:
                self.__board[i] = ReversiStone.EMPTY

        # 次の候補を探す
        i_candidates = []
        for i, _ in enumerate(self.__board.copy()):
            if self.__is_candidate(i, next_stone_kind):
                i_candidates.append(i)

        # 候補を反映させる
        for i_candidate in i_candidates:
            self.__board[i_candidate] = ReversiStone.CANDIDATE
        self.__i_candidates = i_candidates

        if i_candidates:
            return True
        else:
            return False
        

    def __is_candidate(self, i_board: int, put_stone_kind: ReversiStone) -> bool:
        """
        盤面のi_boardにput_stone_kind(BLACK or WHITE)のコマを置けるかどうか
        置けるならTrue、置けなければFalseを返す
        """

        # 空コマ以外なら置けないことが確定
        if self.__board[i_board] != ReversiStone.EMPTY:
            return False

        # 相手のコマ
        enemy_stone_kind = self.__get_reverse_stone_kind(put_stone_kind)

        # 方向パラメータ
        UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
        RIGHT_UP, RIGHT_DOWN, LEFT_UP, LEFT_DOWN = RIGHT+UP, RIGHT+DOWN, LEFT+UP, LEFT+DOWN
        
        # 8方向を走査
        for i_unit in (RIGHT, RIGHT_UP, UP, LEFT_UP, LEFT, LEFT_DOWN, DOWN, RIGHT_DOWN):
            # 置いたコマの隣が敵のコマ出なければ次へ
            i_check = i_board + i_unit
            if self.__board[i_check] != enemy_stone_kind:
                continue

            # 敵のコマである限り、unit_vec方向に進み続ける
            while self.__board[i_check] == enemy_stone_kind:
                i_check += i_unit
            
            # 敵のコマのあとが自分のコマなら置けることが確定
            if self.__board[i_check] == put_stone_kind:
                return True
            
        # 全方向探索してもひっくり返せるコマが見つからなければ置けないことが確定
        return False
