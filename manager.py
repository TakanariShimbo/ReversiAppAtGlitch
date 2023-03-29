from stone import ReversiStone
from controller import ReversiController


class User:
    def __init__(self, session_id: str, room_name: str, stone_kind: ReversiStone) -> None:
        self.__session_id = session_id
        self.__room_name = room_name
        self.__stone_kind = stone_kind
        
    @property
    def session_id(self) -> str:
        return self.__session_id
    
    @property
    def room_name(self) -> str:
        return self.__room_name
    
    @property
    def stone_kind(self) -> ReversiStone:
        return self.__stone_kind
    

class Room:
    def __init__(self, room_name: str, controller: ReversiController) -> None:
        self.__room_name = room_name
        self.__controller = controller
        self.__players = {}

    @property
    def room_name(self) -> str:
        return self.__room_name

    @property
    def players(self):
        return self.__players

    @property
    def controller(self) -> ReversiController:
        return self.__controller

    def add_player(self, stone_kind: ReversiStone,session_id: str) -> None:
        self.__players[stone_kind] = session_id

    def remove_player(self, stone_kind: ReversiStone) -> None:
        del self.__players[stone_kind]

    def is_empty(self) -> bool:
        return len(self.__players) == 0

    def is_full(self) -> bool:
        return len(self.__players) == 2
    
    def get_empty_stone_kind(self) -> ReversiStone:
        return ({ReversiStone.BLACK, ReversiStone.WHITE} - set(self.__players.keys())).pop()


class RoomUserManager:
    def __init__(self):
        self.__room_dict = {}
        self.__user_dict = {}

    def get_user(self, session_id: str) -> User:
        return self.__user_dict.get(session_id)
    
    def get_room(self, room_name: str) -> Room:
        return self.__room_dict.get(room_name)
    
    @property
    def room_name_list(self):
        return list(self.__room_dict.keys())

    def can_enter_room(self, room_name: str) -> bool:
        if room_name in self.room_name_list:
            return True
        else:
            return False

    def can_create_room(self, room_name: str) -> bool:
        if room_name in self.room_name_list:
            return False
        return True
    
    def create_room(self, room_name: str) -> None:
        room = Room(room_name, ReversiController())
        self.__room_dict[room_name] = room        

    def create_user_and_assign_to_room(self, session_id: str, room_name: str, stone_kind: ReversiStone) -> None:
        self.__create_user(session_id, room_name, stone_kind)
        self.__assign_to_room(room_name, stone_kind, session_id)

    def __create_user(self, session_id, room_name, stone_kind):
        user = User(session_id, room_name, stone_kind)
        self.__user_dict[session_id] = user

    def __assign_to_room(self, room_name, stone_kind, session_id):
        room = self.get_room(room_name)
        room.add_player(stone_kind, session_id)

    def remove_user(self, session_id: str) -> None:
        user = self.get_user(session_id)
        room = self.get_room(user.room_name)

        self.__remove_user(session_id)
        room.remove_player(user.stone_kind)

    def __remove_user(self, session_id):
        del self.__user_dict[session_id]

    def remove_room(self, room_name: str) -> None:
        room = self.__room_dict.get(room_name)

        for session_id in room.players.values():
            self.remove_user(session_id)
        self.__remove_room(room_name)

    def __remove_room(self, room_name):
        del self.__room_dict[room_name]