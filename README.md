# Password Generator

A small command-line tool that prints strong random passwords. It uses Python's
`secrets` module, the standard library's cryptographically secure source of
randomness, so the output is suitable for real accounts. There is nothing to
install.

## Requirements

Python 3.8 or newer. Nothing else.

## Usage

```bash
python3 password_generator.py
```

That prints one 20-character password:

```
D<C}O5w&kIM%x(MAaNp#
```

### Options

| Option | Default | Meaning |
| --- | --- | --- |
| `-l`, `--length` | `20` | Number of characters in each password |
| `-n`, `--count` | `1` | How many passwords to print |
| `--no-digits` | off | Leave out digits `0-9` |
| `--no-symbols` | off | Leave out punctuation symbols |
| `--no-ambiguous` | off | Leave out easily confused characters such as `l`, `1`, `O` and `0` |

### Examples

Five passwords of 32 characters, for a password manager's master list:

```bash
python3 password_generator.py -l 32 -n 5
```

A long letters-and-digits password, for a site that rejects symbols:

```bash
python3 password_generator.py --no-symbols -l 24
```

A password that is easy to read aloud without confusing `l` and `1`:

```bash
python3 password_generator.py --no-ambiguous -l 20
```

## How it works

Every password is guaranteed to contain at least one lowercase letter and one
uppercase letter, plus at least one digit and one symbol unless you turn them
off. Those required characters are picked first, the remainder is filled from
the full set, and the whole thing is shuffled so the required characters are not
stuck at the front. If the requested length is shorter than the number of
required character types, the script refuses with an error instead of quietly
producing a weaker password.

## Notes

- `secrets` is used rather than `random`: `random` is a predictable
  pseudo-random generator and must not be used for passwords.
- With the defaults (length 20, all character types) there are more than
  10^31 possible passwords, so collisions and guessing are not a practical
  concern.
- Output goes to standard output only. Nothing is written to disk and nothing is
  logged, so redirect it somewhere safe if you save it:
  ```bash
  python3 password_generator.py >> ~/.passwords.txt
  ```
