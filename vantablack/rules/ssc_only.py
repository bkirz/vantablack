from rule import Scope, SongRule
from simfile.dir import SimfileDirectory

from vantablack.rule import RuleViolation


class SSCOnly(SongRule):
    name = "ssc_only"
    scope = Scope.SONG

    def __init__(self, _config):
        pass

    def apply(self, song: SimfileDirectory) -> list[RuleViolation]:
        match song.sm_path:
            case None:
                return []
            case _:
                violation = RuleViolation(
                    originating_rule=self,
                    message="Unexpected SM file found at path: {}".format(song.sm_path),
                    target=song,
                )
                return [violation]
