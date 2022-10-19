from rule import Scope, SongRule
from simfile.dir import SimfileDirectory

from vantablack.rule import RuleViolation


class RestrictField(SongRule):
    name = 'restrict_field'
    scope = Scope.SONG

    def __init__(self, config):
        self.field = config['field']
        self.value = config['value']

    def apply(self, song_dir: SimfileDirectory) -> list[RuleViolation]:
        file = song_dir.open()

        return [
           RuleViolation(
                message=f"Found chart {chart.stepstype}/{chart.difficulty} with unexpected {self.field} '{chart[self.field]}'. Expected: {self.value}",
                originating_rule=self,
                target=song_dir,
            )
           for chart in file.charts
           if chart[self.field] != self.value
        ]