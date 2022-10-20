from enum import Enum, unique


@unique
class Scope(Enum):
    PACK = "pack"
    SONG = "song"
    FILE = "file"
    CHART = "chart"
