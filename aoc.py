#!/usr/bin/env python3
import importlib
import sys
from pathlib import Path

import click
import typer

app = typer.Typer(no_args_is_help=True)


python_template = """\
def main(data: str):
    pass
"""


@app.command()
def init(day: str):
    """Create a new AOC challenge solution."""
    day_root = Path(f"day{day}")
    day_root.mkdir(exist_ok=True)

    pyfile = "__init__.py"
    paths = ["data.txt", "example.txt"]
    for p in paths:
        pth = day_root / p
        pth.touch()

    pyfilepth = day_root / pyfile
    if not pyfilepth.exists():
        pyfilepth.write_text(python_template)


def getdata(day: str, *, example: bool):
    name = "data"
    if example:
        name = "example"

    file = Path(f"day{day}/{name}.txt")
    try:
        return file.read_text()
    except FileNotFoundError:
        raise click.FileError(str(file), "File does not exist")


@app.command()
def run(day: str, example: bool = False):
    """Run an aoc challenge"""
    data = getdata(day, example=example)
    return importlib.import_module(f"day{day}").main(data)


if __name__ == "__main__":
    sys.exit(app())
