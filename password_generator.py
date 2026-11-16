#!/usr/bin/env python3
"""Generate strong random passwords using the standard library's secrets module.

Examples:
    python3 password_generator.py                 # one 20-character password
    python3 password_generator.py -l 32 -n 5      # five 32-character passwords
    python3 password_generator.py --no-symbols    # letters and digits only
    python3 password_generator.py --no-ambiguous  # skip look-alike characters
"""

from __future__ import annotations

import argparse
import secrets
import string
import sys

AMBIGUOUS = "Il1O|0Oo`'\";:,."
SYMBOLS = "!@#$%^&*()-_=+[]{}<>?/~"


def build_pools(use_digits: bool, use_symbols: bool, exclude_ambiguous: bool):
    """Return the character pools that at least one character must come from."""
    pools = [string.ascii_lowercase, string.ascii_uppercase]
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(SYMBOLS)

    if exclude_ambiguous:
        pools = ["".join(c for c in pool if c not in AMBIGUOUS) for pool in pools]

    return pools


def generate_password(length: int, pools, exclude_ambiguous: bool) -> str:
    """Build a password containing at least one character from every pool."""
    alphabet = "".join(pools)
    if exclude_ambiguous:
        alphabet = "".join(c for c in alphabet if c not in AMBIGUOUS)

    # One character from each required pool, then fill the rest from everything.
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate strong random passwords.",
        epilog="Passwords come from the secrets module, not random.",
    )
    parser.add_argument(
        "-l", "--length", type=int, default=20,
        help="number of characters (default: 20)",
    )
    parser.add_argument(
        "-n", "--count", type=int, default=1,
        help="how many passwords to print (default: 1)",
    )
    parser.add_argument(
        "--no-digits", action="store_true",
        help="leave out digits 0-9",
    )
    parser.add_argument(
        "--no-symbols", action="store_true",
        help="leave out punctuation symbols",
    )
    parser.add_argument(
        "--no-ambiguous", action="store_true",
        help="leave out easily confused characters such as l, 1, O and 0",
    )
    args = parser.parse_args(argv)

    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.length < 1:
        parser.error("--length must be at least 1")

    pools = build_pools(
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        exclude_ambiguous=args.no_ambiguous,
    )

    if args.length < len(pools):
        sys.exit(
            f"length {args.length} is too short for {len(pools)} required "
            "character types; use a longer password or more --no-* flags"
        )

    for _ in range(args.count):
        print(generate_password(args.length, pools, args.no_ambiguous))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
