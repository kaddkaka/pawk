#!/usr/bin/env python3

from argparse import ArgumentParser

parser = ArgumentParser(prog='Pawk', description='awk-like python tool')
parser.add_argument("program")
parser.add_argument("file")
args = parser.parse_args()

with open(args.file, encoding="utf8") as infile:
    for line in infile:
        f = line.split()
        l = {"f": f}
        exec(args.program, {}, l)
