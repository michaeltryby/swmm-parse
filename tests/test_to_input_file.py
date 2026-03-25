#
#  test_to_input_file.py
#
#  Created: Apr 25, 2024
#  Updated: Mar 24, 2026
#
#  Author:  Michael E. Tryby
#           US EPA - ORD/CESER
#

import os
from io import StringIO

import pytest
from lark import Lark

import swmm.parse.to_input_file as sltf

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
EXAMPLE_PROJECT = os.path.join(DATA_PATH, "example-project.inp")
EXPECTED_OUTPUT = os.path.join(DATA_PATH, "expected-output.txt")


def test_to_input_file():

    # Read expected output from file
    with open(EXPECTED_OUTPUT, "r") as file:
        expected = file.read()

    # Convert input file to parse tree
    parser = Lark.open_from_package(
        "swmm.parse", "input-lalr.lark", ("grammars",), parser="lalr"
    )

    with open(EXAMPLE_PROJECT) as f:
        file_tree = parser.parse(f.read())

    # Convert parse tree to inputfile
    tree_to_file = sltf.ToInputFile()
    tree_to_file.visit_topdown(file_tree)

    # Get the captured output as a string
    output = tree_to_file.export()

    assert expected == output
