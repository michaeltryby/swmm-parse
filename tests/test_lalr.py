#
#  test_lalr.py
#
#  Created: Apr 25, 2024
#  Updated:
#
#  Author:  Michael E. Tryby
#           US EPA - ORD/CESER
#

import os

from lark import Lark
import pytest


DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
EXAMPLE_PROJECT = os.path.join(DATA_PATH, 'example-project.inp')
EXPECTED_TREE = os.path.join(DATA_PATH, 'expected-lalr.txt')


def test_lalr(mocker):

    # Read expected tree from file
    with open(EXPECTED_TREE, 'r') as file:
        expected = file.read().strip()

    # Convert input file to parse tree
    parser = Lark.open_from_package(
        "swmm.parse", "input-lalr.lark", ("grammars",), parser="lalr"
    )

    # Create parse tree and convert to string
    with open(EXAMPLE_PROJECT) as f:
        file_tree = parser.parse(f.read())

    output = str(file_tree).strip()

    assert expected == output
