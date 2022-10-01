from simfile.dir import SimfileDirectory
from rule import SongRule, Scope

from vantablack.rule import RuleViolation

class RequireChart(SongRule):
    name = 'require_difficulty'
    scope = Scope.SONG

    def __init__(self, config):
        self.difficulty = config['difficulty']
        self.style = config['style']

    def apply(self, song_dir: SimfileDirectory) -> list[RuleViolation]:
        # TODO: This type of API will need to open a lot of song dirs.
        # Perhaps there should be a difference in scope between song dir and opened song?
        # Internal, maybe?
        file = song_dir.open()

        matching_charts = filter(
            lambda c: c.difficulty == self.difficulty and c.style == self.style,
            file.charts
        )

        if matching_charts:
            return []
        else: 
            return [RuleViolation(
                message=f"Difficulty {self.difficulty} for style {self.style} not present in file.",
                originating_rule=self,
                target=song_dir,
            )]