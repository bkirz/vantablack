import operator
import os

from rule import Scope, SongRule
from simfile.dir import SimfileDirectory

from vantablack.rule import RuleViolation


class NoExtraFiles(SongRule):
    name = "no_extra_files"
    scope = Scope.SONG

    ASSET_KEYS = [
        "music",
        "banner",
        "background",
        "cdtitle",
        "jacket",
        "cdimage",
        "disc",
    ]

    def __init__(self, config):
        self.allowed_exceptions = config.get("allow", [])

    def apply(self, song: SimfileDirectory) -> list[RuleViolation]:
        song_dir = song.simfile_dir

        expected_file_paths: list[str] = filter(
            lambda path: path is not None,
            [
                *operator.attrgetter(*self.ASSET_KEYS)(song.assets()),
                *self.allowed_exceptions,
                song.sm_path,
                song.ssc_path,
            ],
        )

        normalized_expected_files = [
            os.path.relpath(p, song_dir) for p in expected_file_paths
        ]

        actual_files = [p for p in os.listdir(song.simfile_dir)]
        unexpected_files = [
            path for path in actual_files if path not in normalized_expected_files
        ]

        return [
            RuleViolation(
                originating_rule=self,
                target=song,
                message=f"Found unexpected non-simfile, non-asset file '{file}'.",
            )
            for file in unexpected_files
        ]
