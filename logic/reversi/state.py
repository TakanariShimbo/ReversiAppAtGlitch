from enum import Enum, auto


class ReversiState(Enum):
    PLAYING = auto()
    FINISHED = auto()