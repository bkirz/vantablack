from rule import Scope, SongRule
from simfile.dir import SimfileDirectory

from vantablack.rule import RuleViolation


class RequireCredit(SongRule):
    name = "require_credit"
    scope = Scope.SONG

    def __init__(self, config):
        self.value = config["value"]

    def apply(self, song_dir: SimfileDirectory) -> list[RuleViolation]:
        file = song_dir.open()

        return [
            RuleViolation(
                message=f"Chart {chart.stepstype}/{chart.difficulty} has credit '{chart.credit}'. Expected: '{self.value}'",
                originating_rule=self,
                target=song_dir,
            )
            for chart in file.charts
            if chart.credit != self.value
        ]
