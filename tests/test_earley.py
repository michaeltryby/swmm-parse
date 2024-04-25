#
#  test_earley.py
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


DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
EXAMPLE_PROJECT = os.path.join(DATA_PATH, 'example-project.inp')


def test_early(mocker):

    expected = """Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'section'), [Token('KEYWORD', 'TITLE'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'Example')]), Tree('keyword', [Token('KEYWORD', 'SWMM')]), Tree('keyword', [Token('KEYWORD', 'Project')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'OPTIONS'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'FLOW_UNITS')]), Tree('keyword', [Token('KEYWORD', 'CFS')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'INFILTRATION')]), Tree('keyword', [Token('KEYWORD', 'GREEN_AMPT')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'FLOW_ROUTING')]), Tree('keyword', [Token('KEYWORD', 'KINWAVE')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'START_DATE')]), Tree('date', [Token('DATE', '8/6/2002')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'START_TIME')]), Tree('time', [Token('TIME', '10:00')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'END_TIME')]), Tree('time', [Token('TIME', '18:00')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'WET_STEP')]), Tree('time', [Token('TIME', '00:15:00')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'DRY_STEP')]), Tree('time', [Token('TIME', '01:00:00')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'ROUTING_STEP')]), Tree('time', [Token('TIME', '00:05:00')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'RAINGAGES'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'GAGE1')]), Tree('keyword', [Token('KEYWORD', 'INTENSITY')]), Tree('time', [Token('TIME', '0:15')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('keyword', [Token('KEYWORD', 'TIMESERIES')]), Tree('name', [Token('NAME', 'SERIES1')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'EVAPORATION'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'CONSTANT')]), Tree('float', [Token('FLOAT', '0.02')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'SUBCATCHMENTS'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA1')]), Tree('name', [Token('NAME', 'GAGE1')]), Tree('name', [Token('NAME', 'NODE1')]), Tree('integer', [Token('INTEGER', '2')]), Tree('float', [Token('FLOAT', '80.0')]), Tree('float', [Token('FLOAT', '800.0')]), Tree('float', [Token('FLOAT', '1.0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA2')]), Tree('name', [Token('NAME', 'GAGE1')]), Tree('name', [Token('NAME', 'NODE2')]), Tree('integer', [Token('INTEGER', '2')]), Tree('float', [Token('FLOAT', '75.0')]), Tree('float', [Token('FLOAT', '50.0')]), Tree('float', [Token('FLOAT', '1.0')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'SUBAREAS'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA1')]), Tree('float', [Token('FLOAT', '0.2')]), Tree('float', [Token('FLOAT', '0.02')]), Tree('float', [Token('FLOAT', '0.02')]), Tree('float', [Token('FLOAT', '0.1')]), Tree('float', [Token('FLOAT', '20.0')]), Tree('keyword', [Token('KEYWORD', 'OUTLET')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA2')]), Tree('float', [Token('FLOAT', '0.2')]), Tree('float', [Token('FLOAT', '0.02')]), Tree('float', [Token('FLOAT', '0.02')]), Tree('float', [Token('FLOAT', '0.1')]), Tree('float', [Token('FLOAT', '20.0')]), Tree('keyword', [Token('KEYWORD', 'OUTLET')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'INFILTRATION'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA1')]), Tree('float', [Token('FLOAT', '4.0')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('float', [Token('FLOAT', '0.34')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA2')]), Tree('float', [Token('FLOAT', '4.0')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('float', [Token('FLOAT', '0.34')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'JUNCTIONS'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE1')]), Tree('float', [Token('FLOAT', '10.0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE2')]), Tree('float', [Token('FLOAT', '10.0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE3')]), Tree('float', [Token('FLOAT', '5.0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE4')]), Tree('float', [Token('FLOAT', '5.0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE6')]), Tree('float', [Token('FLOAT', '1.0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE7')]), Tree('float', [Token('FLOAT', '2.0')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'DIVIDERS'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'NODE5')]), Tree('float', [Token('FLOAT', '3.0')]), Tree('name', [Token('NAME', 'C6')]), Tree('keyword', [Token('KEYWORD', 'CUTOFF')]), Tree('float', [Token('FLOAT', '1.0')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'CONDUITS'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C1')]), Tree('name', [Token('NAME', 'NODE1')]), Tree('name', [Token('NAME', 'NODE3')]), Tree('integer', [Token('INTEGER', '800')]), Tree('float', [Token('FLOAT', '0.01')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C2')]), Tree('name', [Token('NAME', 'NODE2')]), Tree('name', [Token('NAME', 'NODE4')]), Tree('integer', [Token('INTEGER', '800')]), Tree('float', [Token('FLOAT', '0.01')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C3')]), Tree('name', [Token('NAME', 'NODE3')]), Tree('name', [Token('NAME', 'NODE5')]), Tree('integer', [Token('INTEGER', '400')]), Tree('float', [Token('FLOAT', '0.01')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C4')]), Tree('name', [Token('NAME', 'NODE4')]), Tree('name', [Token('NAME', 'NODE5')]), Tree('integer', [Token('INTEGER', '400')]), Tree('float', [Token('FLOAT', '0.01')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C5')]), Tree('name', [Token('NAME', 'NODE5')]), Tree('name', [Token('NAME', 'NODE6')]), Tree('integer', [Token('INTEGER', '600')]), Tree('float', [Token('FLOAT', '0.01')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C6')]), Tree('name', [Token('NAME', 'NODE5')]), Tree('name', [Token('NAME', 'NODE7')]), Tree('integer', [Token('INTEGER', '400')]), Tree('float', [Token('FLOAT', '0.01')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'XSECTIONS'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C1')]), Tree('keyword', [Token('KEYWORD', 'RECT_OPEN')]), Tree('float', [Token('FLOAT', '0.5')]), Tree('integer', [Token('INTEGER', '1')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C2')]), Tree('keyword', [Token('KEYWORD', 'RECT_OPEN')]), Tree('float', [Token('FLOAT', '0.5')]), Tree('integer', [Token('INTEGER', '1')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C3')]), Tree('keyword', [Token('KEYWORD', 'CIRCULAR')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C4')]), Tree('keyword', [Token('KEYWORD', 'RECT_OPEN')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C5')]), Tree('keyword', [Token('KEYWORD', 'PARABOLIC')]), Tree('float', [Token('FLOAT', '1.5')]), Tree('float', [Token('FLOAT', '2.0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'C6')]), Tree('keyword', [Token('KEYWORD', 'PARABOLIC')]), Tree('float', [Token('FLOAT', '1.5')]), Tree('float', [Token('FLOAT', '2.0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'POLLUTANTS'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'TSS')]), Tree('keyword', [Token('KEYWORD', 'MG/L')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'Lead')]), Tree('keyword', [Token('KEYWORD', 'UG/L')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('keyword', [Token('KEYWORD', 'NO')]), Tree('keyword', [Token('KEYWORD', 'TSS')]), Tree('float', [Token('FLOAT', '0.20')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'LANDUSES'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'RESIDENTIAL')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'UNDEVELOPED')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'WASHOFF'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'RESIDENTIAL')]), Tree('keyword', [Token('KEYWORD', 'TSS')]), Tree('keyword', [Token('KEYWORD', 'EMC')]), Tree('float', [Token('FLOAT', '23.4')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])]), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'UNDEVELOPED')]), Tree('keyword', [Token('KEYWORD', 'TSS')]), Tree('keyword', [Token('KEYWORD', 'EMC')]), Tree('float', [Token('FLOAT', '12.1')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')]), Tree('integer', [Token('INTEGER', '0')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'COVERAGES'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA1')]), Tree('keyword', [Token('KEYWORD', 'RESIDENTIAL')]), Tree('integer', [Token('INTEGER', '80')]), Tree('keyword', [Token('KEYWORD', 'UNDEVELOPED')]), Tree('integer', [Token('INTEGER', '20')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'AREA2')]), Tree('keyword', [Token('KEYWORD', 'RESIDENTIAL')]), Tree('integer', [Token('INTEGER', '55')]), Tree('keyword', [Token('KEYWORD', 'UNDEVELOPED')]), Tree('integer', [Token('INTEGER', '45')])])]), Tree(Token('RULE', 'section'), [Token('KEYWORD', 'TIMESERIES'), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'SERIES1')]), Tree('time', [Token('TIME', '0:00')]), Tree('float', [Token('FLOAT', '0.1')]), Tree('time', [Token('TIME', '0:15')]), Tree('float', [Token('FLOAT', '1.0')]), Tree('time', [Token('TIME', '0:30')]), Tree('float', [Token('FLOAT', '0.5')])]), Tree(Token('RULE', 'record'), [Tree('name', [Token('NAME', 'SERIES1')]), Tree('time', [Token('TIME', '0:45')]), Tree('float', [Token('FLOAT', '0.1')]), Tree('time', [Token('TIME', '1:00')]), Tree('float', [Token('FLOAT', '0.0')]), Tree('time', [Token('TIME', '2:00')]), Tree('float', [Token('FLOAT', '0.0')])])])])\n"""

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
    print(file_tree)

    output = captured_output.getvalue()

    assert expected == output