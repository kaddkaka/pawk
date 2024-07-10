#!/usr/bin/env python3

""" pawk - awk-like python tool"""

from argparse import ArgumentParser
from typing import Any

parser = ArgumentParser(prog='Pawk', description='awk-like python tool')

program_group = parser.add_mutually_exclusive_group(required=True)
program_group.add_argument("-t", "--program-text")
program_group.add_argument("-f", "--program-file")
parser.add_argument("file", nargs="+")
args = parser.parse_args()

if (program := args.program_text) is None:
    with open(args.program_file, encoding="utf8") as program_file:
        program = program_file.read()

def intify(word):
    try:
        return int(word)
    except ValueError:
        return word

_locals: dict[Any, Any] = {"BEGIN": True, "NR": 1}

for file_no, _file in enumerate(args.file):
    last_file = file_no == len(args.file) - 1
    with open(_file, encoding="utf8") as infile:
        lines = infile.read().splitlines()

    for line_no, line in enumerate(lines):
        last_line = line_no == len(lines) - 1
        _locals["END"] = last_file and last_line
        _locals["FNR"] = line_no + 1

        # Full line as f[0] and the rest of columns start from f[1]
        f = [line, *(intify(w) for w in line.split())]
        _locals["F"] = f

        # Poor mans way of implementing "keywords" by catching NameError
        try:
            exec(program, {}, _locals)  # pylint: disable=exec-used
        except NameError as e:
            if str(e) == "name 'NEXT' is not defined":
                pass
            else:
                raise

        _locals["BEGIN"] = False
        _locals["NR"]    += 1
