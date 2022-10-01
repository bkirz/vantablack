import sys, os

import toml
from simfile.dir import SimfilePack

import registry
from rules import ssc_only, require_chart, require_credit, restrict_field
from vantablack.rule import RuleViolation, SongRule

__version__ = "0.1.0"
CONFIG_FILENAME = 'vantablack.toml'

def main(path_to_pack_dir: str):
    # TODO: Where should the top-level registry be defined? How
    # should plugins add their own rules?
    rule_registry = registry.Registry([
        ssc_only.SSCOnly,
        require_chart.RequireChart,
        require_credit.RequireCredit,
        restrict_field.RestrictField,
    ])

    pack = SimfilePack(path_to_pack_dir)

    path_to_config = os.path.join(path_to_pack_dir, CONFIG_FILENAME)

    # TODO: gracefully handle missing file
    with open(path_to_config) as f:
        # TODO: gracefully handle malformed file
        raw_config = toml.load(f)

    rules: list[SongRule] = []
    for scope, rule_configs in raw_config['rules'].items():
        for rule_name, rule_config in rule_configs.items():
            # print("Evaluating rule '{}' with scope '{}' and config '{}'".format(rule_name, scope, rule_config))

            rule_class = rule_registry.rule_class(rule_name)
            if rule_class:
                # TODO: incorporate scope into this, somehow?
                rules.append(rule_class(rule_config))
            else:
                # print("  Unrecognized rule '{}', skipping.".format(rule_name))
                pass
    
    all_violations: RuleViolation = []

    simfile_dirs = sorted(pack.simfile_dirs(), key=lambda song: song.simfile_dir)

    print(f"Validating {len(simfile_dirs)} songs...")

    for song_dir in simfile_dirs:
        song_violations = []

        formatted_dir_name = os.path.split(song_dir.simfile_dir)[-1]
        print(formatted_dir_name, '  ', end='')

        for rule in rules:
            rule_violations = rule.apply(song_dir)
            if len(rule_violations) == 0:
                print('.', end='')
            else:
                print('F', end='')

            song_violations.extend(rule_violations)

        print('')

        for violation in song_violations:
            print('  ', violation.message)
        
        all_violations.extend(song_violations)


# python vantablack.py ~/stepmania_songs/my_pack
if __name__ == "__main__":
    main(sys.argv[1])
