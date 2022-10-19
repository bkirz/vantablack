from enum import Enum, unique


@unique
class Scope(Enum):
    _ignore_ = "_SCOPE_HIERARCHY"

    PACK = "pack"
    SONG = "song"
    # FILE = 'file'
    # CHART = 'chart'

    _SCOPE_HIERARCHY: dict["Scope", list["Scope"]] = {
        PACK: [SONG],
    }

    def __gt__(self, other: "Scope") -> bool:
        if other == self:
            return False

        descendants = self._SCOPE_HIERARCHY.get(self, [])
        if other in descendants:
            return True

        return any(descendant > other for descendant in descendants)
