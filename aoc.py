#!/usr/bin/python3
import argparse
import sys
import importlib


def getdata(day: str, *, example=False):
    suffix = ""
    if example:
        suffix = ".example"

    file = f"data/day{day}{suffix}.txt"
    try:
        with open(file) as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERR: Could not load data file {file}.", file=sys.stderr)
        sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=str)
    parser.add_argument("--example", action="store_true")

    return parser.parse_args()


def main(args):
    data = getdata(args.day, example=args.example)
    importlib.import_module(f"day{args.day}").main(data)


if __name__ == "__main__":
    sys.exit(main(get_args()))
