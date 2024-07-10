#!/usr/bin/env python3

""" pawk - awk-like python tool"""

from argparse import ArgumentParser
from typing import Any

parser = ArgumentParser(prog='Pawk', description='awk-like python tool')

program_group = parser.add_mutually_exclusive_group(required=True)
program_group.add_argument("-t", "--program-text")
program_group.add_argument("-f", "--program-file")
parser.add_argument("file")
args = parser.parse_args()

if (program := args.program_text) is None:
    with open(args.program_file, encoding="utf8") as program_file:
        program = program_file.read()

with open(args.file, encoding="utf8") as infile:
    lines = infile.read().splitlines()

def intify(word):
    try:
        return int(word)
    except ValueError:
        return word


_locals: dict[Any, Any] = {}
for i, line in enumerate(lines):
    _locals["BEGIN"] = i == 0
    _locals["END"]   = i == len(lines) - 1
    _locals["NR"]    = i + 1

    # Full line as f[0] and the rest of columns start from f[1]
    f = [line, *(intify(w) for w in line.split())]
    _locals["F"] = f

    exec(program, {}, _locals)  # pylint: disable=exec-used
