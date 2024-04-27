#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3

# NOTE: Requires Python 3+
# usage: drunken_bishop.py [-h] [--mode {md5,sha256}] fingerprint
#
# Generate randomart from fingerprint
#
# positional arguments:
#   fingerprint
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --mode {md5,sha256}, -m {md5,sha256}

# source: https://stackoverflow.com/a/41208301/5742216

import argparse
import base64


def simulate_bishop_stumbles(steps):
    field = [[0] * 17 for _ in range(9)]
    start_position = (4, 8)
    direction_map = {
        "00": (-1, -1),
        "01": (-1, 1),
        "10": (1, -1),
        "11": (1, 1),
    }

    def clip_at_walls(x, y):
        return min(max(x, 0), 8), min(max(y, 0), 16)

    pos = start_position
    for step in steps:
        x, y = pos
        field[x][y] += 1
        dx, dy = direction_map[step]
        pos = clip_at_walls(x + dx, y + dy)

    x, y = start_position
    field[x][y] = 15
    x, y = pos
    field[x][y] = 16

    return field


def get_steps(fingerprint_bytes):
    return [
        "{:02b}".format(b >> s & 3) for b in fingerprint_bytes for s in (0, 2, 4, 6)
    ]


def print_randomart(atrium, hash_mode):
    # Symbols for the number of times a position is visited by the bishop
    # White space means that the position was never visited
    # S and E are the start and end positions
    value_symbols = " .o+=*BOX@%&#/^SE"

    print("+---[   n/a  ]----+")
    for row in atrium:
        symbolic_row = [value_symbols[visits] for visits in row]
        print("|" + "".join(symbolic_row) + "|")
    print("+" + ("[" + hash_mode.upper() + "]").center(17, "-") + "+")


def get_bytes(fingerprint, hash_mode):
    if hash_mode == "md5":
        return [int(i, 16) for i in fingerprint.split(":")]
    elif hash_mode == "sha256":
        missing_padding = 4 - (len(fingerprint) % 4)
        fingerprint += "=" * missing_padding
        return base64.b64decode(fingerprint)
    elif hash_mode == "sha256hex":
        return base64.b16decode(fingerprint, casefold=True)
    raise RuntimeError("Unsupported hashing mode: {}".format(hash_mode))


def get_argparser():
    parser = argparse.ArgumentParser(description="Generate randomart from fingerprint")
    parser.add_argument("--mode", "-m", choices=["md5", "sha256"], default="sha256hex")
    parser.add_argument("fingerprint", type=str)
    return parser


def drunken_bishop(fingerprint, hash_mode):
    fingerprint_bytes = get_bytes(fingerprint, hash_mode)
    steps = get_steps(fingerprint_bytes)
    atrium_state = simulate_bishop_stumbles(steps)
    print_randomart(atrium_state, hash_mode)


if __name__ == "__main__":
    parser = get_argparser()
    args = parser.parse_args()
    drunken_bishop(args.fingerprint, args.mode)
