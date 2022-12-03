#!/usr/bin/env python3
import sys
import importlib
import typer
import click

from pathlib import Path

app = typer.Typer(no_args_is_help=True)


python_template = """\
def main(data: str):
    pass
"""


@app.command()
def init(day: str):
    """Create a new AOC challenge solution."""
    pyfile = "day{}.py"
    paths = ["data/day{}.txt", "data/day{}.example.txt"]
    for p in paths:
        pth = Path(p.format(day))
        pth.touch()

    pyfilepth = Path(pyfile.format(day))
    if not pyfilepth.exists():
        pyfilepth.write_text(python_template)


def getdata(day: str, *, example: bool):
    suffix = ""
    if example:
        suffix = ".example"

    file = Path(f"data/day{day}{suffix}.txt")
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
