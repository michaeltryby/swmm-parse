#
#  test_to_input_file.py
#
#  Created: Apr 25, 2024
#  Updated:
#
#  Author:  Michael E. Tryby
#           US EPA - ORD/CESER
#


import os
from io import StringIO

from lark import Lark
import pytest

import swmm.parse.to_input_file as sltf


DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
EXAMPLE_PROJECT = os.path.join(DATA_PATH, 'example-project.inp')


def test_to_input_file(mocker):

    expected = """\n[TITLE]\nExample SWMM Project\n\n[OPTIONS]\nFLOW_UNITS CFS\nINFILTRATION GREEN_AMPT\nFLOW_ROUTING KINWAVE\nSTART_DATE 8/6/2002\nSTART_TIME 10:00\nEND_TIME 18:00\nWET_STEP 00:15:00\nDRY_STEP 01:00:00\nROUTING_STEP 00:05:00\n\n[RAINGAGES]\nGAGE1 INTENSITY 0:15 1.0 TIMESERIES SERIES1\n\n[EVAPORATION]\nCONSTANT 0.02\n\n[SUBCATCHMENTS]\nAREA1 GAGE1 NODE1 2 80.0 800.0 1.0\nAREA2 GAGE1 NODE2 2 75.0 50.0 1.0\n\n[SUBAREAS]\nAREA1 0.2 0.02 0.02 0.1 20.0 OUTLET\nAREA2 0.2 0.02 0.02 0.1 20.0 OUTLET\n\n[INFILTRATION]\nAREA1 4.0 1.0 0.34\nAREA2 4.0 1.0 0.34\n\n[JUNCTIONS]\nNODE1 10.0\nNODE2 10.0\nNODE3 5.0\nNODE4 5.0\nNODE6 1.0\nNODE7 2.0\n\n[DIVIDERS]\nNODE5 3.0 C6 CUTOFF 1.0\n\n[CONDUITS]\nC1 NODE1 NODE3 800 0.01 0 0 0\nC2 NODE2 NODE4 800 0.01 0 0 0\nC3 NODE3 NODE5 400 0.01 0 0 0\nC4 NODE4 NODE5 400 0.01 0 0 0\nC5 NODE5 NODE6 600 0.01 0 0 0\nC6 NODE5 NODE7 400 0.01 0 0 0\n\n[XSECTIONS]\nC1 RECT_OPEN 0.5 1 0 0\nC2 RECT_OPEN 0.5 1 0 0\nC3 CIRCULAR 1.0 0 0 0\nC4 RECT_OPEN 1.0 1.0 0 0\nC5 PARABOLIC 1.5 2.0 0 0\nC6 PARABOLIC 1.5 2.0 0 0\n\n[POLLUTANTS]\nTSS MG/L 0 0 0 0\nLead UG/L 0 0 0 0 NO TSS 0.20\n\n[LANDUSES]\nRESIDENTIAL\nUNDEVELOPED\n\n[WASHOFF]\nRESIDENTIAL TSS EMC 23.4 0 0 0\nUNDEVELOPED TSS EMC 12.1 0 0 0\n\n[COVERAGES]\nAREA1 RESIDENTIAL 80 UNDEVELOPED 20\nAREA2 RESIDENTIAL 55 UNDEVELOPED 45\n\n[TIMESERIES]\nSERIES1 0:00 0.1 0:15 1.0 0:30 0.5\nSERIES1 0:45 0.1 1:00 0.0 2:00 0.0\n"""

    # Convert input file to parse tree
    parser = Lark.open_from_package(
        "swmm.parse", "input-earley.lark", ("grammars",), parser="earley"
    )

    # Create a StringIO object to capture printed output
    captured_output = StringIO()
    # Patch sys.stdout to replace it with the StringIO object
    mocker.patch('sys.stdout', new=captured_output)


    with open(EXAMPLE_PROJECT) as f:
        file_tree = parser.parse(f.read())

    # Convert parse tree to inputfile
    tree_to_file = sltf.ToInputFile()
    tree_to_file.visit_topdown(file_tree)

    # Get the captured output as a string
    tree_to_file.export()
    output = captured_output.getvalue()

    assert expected == output
