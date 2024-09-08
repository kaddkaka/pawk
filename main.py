#!/usr/bin/env python3

""" pawk - awk-like python tool"""

import fileinput
from argparse import ArgumentParser
from typing import Any

def parse_args():
    parser = ArgumentParser(prog='Pawk', description='awk-like python tool')

    program_group = parser.add_mutually_exclusive_group(required=True)
    program_group.add_argument("-t", "--program-text")
    program_group.add_argument("-f", "--program-file")
    parser.add_argument("file", nargs="+")
    return parser.parse_args()


def intify(word):
    """Try to parse as numbers if possible"""
    try:
        return int(word)
    except ValueError:
        return word


def compile_program(args):
    """Compile user program"""
    if (program_src := args.program_text) is None:
        with open(args.program_file, encoding="utf8") as program_file:
            program_src = program_file.read()
    return compile(program_src, args.program_file or "<string>", 'exec')


def iterate_files(files):
    """Iterate over all input files, also supports '-' for STDIN"""
    for file_no, file_ in enumerate(files):
        last_file = file_no == len(files) - 1
        with fileinput.input(file_, encoding="utf8") as infile:
            lines = list(l.rstrip() for l in infile)
        yield lines, last_file


def process_file(program, lines, last_file, _locals):
    """Iterate over multiline text input and process with user program"""
    for line_no, line in enumerate(lines):
        last_line = line_no == len(lines) - 1
        _locals["END"] = last_file and last_line
        _locals["FNR"] = line_no + 1

        # Full line as f[0] and the rest of columns start from f[1]
        f = [line, *(intify(w) for w in line.split())]
        _locals["F"] = f
        _locals["NF"] = len(f)

        # Poor mans way of implementing "keywords" by catching NameError
        try:
            exec(program, {}, _locals)  # pylint: disable=exec-used
        except NameError as e:
            if e.name == "NEXT":
                pass
            else:
                raise

        _locals["BEGIN"] = False
        _locals["NR"]    += 1


def main() -> None:
    """Main"""
    args = parse_args()
    program = compile_program(args)
    _locals: dict[Any, Any] = {"BEGIN": True, "NR": 1}
    for lines, last_file in iterate_files(args.file):
        process_file(program, lines, last_file, _locals)


if __name__ == "__main__":
    main()
