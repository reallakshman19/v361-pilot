"""Count whitespace-separated words in a UTF-8 text file."""
import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Count whitespace-separated words in a text file."
    )
    parser.add_argument("file", help="Path to the text file")
    args = parser.parse_args(argv)

    try:
        with open(args.file, "r", encoding="utf-8") as stream:
            count = sum(len(line.split()) for line in stream)
    except (OSError, UnicodeError) as exc:
        print(f"wordcount: {exc}", file=sys.stderr)
        return 1

    print(count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
