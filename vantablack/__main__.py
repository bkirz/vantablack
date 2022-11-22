import os
from typing import Any

import runner

import argparse

__version__ = "0.1.0"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--pack", type=str, dest="pack")
    group.add_argument("-s", "--song", type=str, dest="song")

    args = parser.parse_args()

    if args.pack is not None:
        runner.validate_pack(os.path.abspath(args.pack))

    if args.song is not None:
        runner.validate_song(os.path.abspath(args.song))
