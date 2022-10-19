from rule import Scope, SongRule
from simfile.dir import SimfileDirectory

from vantablack.rule import RuleViolation


class OggOnly(SongRule):
    name = 'ogg_only'
    scope = Scope.SONG

    def __init__(self, _config):
        pass

    def apply(self, song_dir: SimfileDirectory) -> list[RuleViolation]:
        music_path = song_dir.assets().music

        if not music_path.endswith('.ogg'):
            return [RuleViolation(
                message=f"Found non-ogg music file: {music_path}",
                originating_rule=self,
                target=song_dir,
            )]
        else:
            return []
