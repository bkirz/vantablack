from typing import Any
import toml
import os
from vantablack.registry import Registry
from vantablack.rule import RuleViolation, SongRule
from vantablack.rules import (
    ssc_only,
    require_chart,
    require_credit,
    restrict_field,
    no_extra_files,
    ogg_only,
)
from simfile.dir import SimfileDirectory, SimfilePack


CONFIG_FILENAME = "vantablack.toml"


def build_registry():
    # TODO: Where should the top-level registry be defined? How
    # should plugins add their own rules?
    return Registry.Registry(
        [
            ssc_only.SSCOnly,
            require_chart.RequireChart,
            require_credit.RequireCredit,
            restrict_field.RestrictField,
            no_extra_files.NoExtraFiles,
            ogg_only.OggOnly,
        ]
    )


def load_config(path):
    print(f"Loading config from {path}")
    # TODO: gracefully handle missing file
    with open(path) as f:
        # TODO: gracefully handle malformed file
        return toml.load(f)


def build_rules(rule_registry: Registry, raw_config: dict[str, Any]) -> list[SongRule]:
    rules: list[SongRule] = []
    for scope, rule_configs in raw_config["rules"].items():
        for rule_name, rule_config in rule_configs.items():
            rule_class = rule_registry.rule_class(rule_name)
            if rule_class:
                # TODO: incorporate scope into this, somehow?
                rules.append(rule_class(rule_config))
            else:
                print(f"  Unrecognized rule '{rule_name}', skipping.")
                pass

    return rules


def validate_pack(path_to_pack_dir: str):
    rule_registry = build_registry()

    pack = SimfilePack(path_to_pack_dir)
    path_to_config = os.path.join(path_to_pack_dir, CONFIG_FILENAME)
    raw_config = load_config(path_to_config)

    rules = build_rules(rule_registry, raw_config)

    all_violations: RuleViolation = []

    simfile_dirs = sorted(pack.simfile_dirs(), key=lambda song: song.simfile_dir)
    print(f"Validating {len(simfile_dirs)} songs...")

    for song_dir in simfile_dirs:
        song_violations = check_song(song_dir, rules)
        all_violations.extend(song_violations)


def validate_song(path_to_song_dir: str):
    rule_registry = build_registry()

    song = SimfileDirectory(path_to_song_dir)
    (path_to_pack_dir, _song_dir_name) = os.path.split(path_to_song_dir)
    path_to_config = os.path.join(path_to_pack_dir, CONFIG_FILENAME)
    raw_config = load_config(path_to_config)

    rules = build_rules(rule_registry, raw_config)

    check_song(song, rules)


def check_song(
    song_dir: SimfileDirectory, rules: list[SongRule]
) -> list[RuleViolation]:
    song_violations = []

    (_prefix, formatted_dir_name) = os.path.split(song_dir.simfile_dir)
    print(formatted_dir_name, "  ", end="")

    for rule in rules:
        rule_violations = rule.apply(song_dir)
        if len(rule_violations) == 0:
            print(".", end="")
        else:
            print("F", end="")

        song_violations.extend(rule_violations)

    print("")

    for violation in song_violations:
        print("  ", violation.message)

    return song_violations
