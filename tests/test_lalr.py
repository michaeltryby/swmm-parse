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

import pytest
from lark import Lark

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
EXAMPLE_PROJECT = os.path.join(DATA_PATH, "example-project.inp")
EXPECTED_TREE = os.path.join(DATA_PATH, "expected-lalr.txt")


SECTION_CASES = [
    ("TITLE", "[TITLE]\nProject Title\n"),
    ("OPTIONS", "[OPTIONS]\nFLOW_UNITS CFS\n"),
    ("JUNCTIONS", "[JUNCTIONS]\nJ1 100 10 0 0 0\n"),
    ("OUTFALLS", "[OUTFALLS]\nO1 95 FREE\n"),
    ("DIVIDERS", "[DIVIDERS]\nD1 100 C1 CUTOFF 1.0\n"),
    ("STORAGE", "[STORAGE]\nS1 100 10 0 TABULAR 1\n"),
    ("CONDUITS", "[CONDUITS]\nC1 J1 J2 1000 0.013 0 0\n"),
    ("PUMPS", "[PUMPS]\nP1 J1 J2 CURVE1 ON 1.0 0.5\n"),
    ("ORIFICES", "[ORIFICES]\nOR1 J1 J2 SIDE 1.0 0.62 YES 0.0\n"),
    ("WEIRS", "[WEIRS]\nW1 J1 J2 TRANSVERSE 1.0 3.2 NO\n"),
    ("OUTLETS", "[OUTLETS]\nOUT1 J1 J2 0.0 TABULAR CURVE1 NO\n"),
    ("XSECTIONS", "[XSECTIONS]\nC1 CIRCULAR 1.0\n"),
    ("TRANSECTS", "[TRANSECTS]\nNC 0.03 0.03 0.03\n"),
    ("LOSSES", "[LOSSES]\nC1 0.1 0.1 0.1 NO 0.0\n"),
    ("RAINGAGES", "[RAINGAGES]\nRG1 INTENSITY 0:05 1.0 TIMESERIES TS1\n"),
    ("SUBCATCHMENTS", "[SUBCATCHMENTS]\nS1 RG1 J1 10.0 50 500 1.0 0.0\n"),
    ("SUBAREAS", "[SUBAREAS]\nS1 0.01 0.1 1.0 5.0 25 OUTLET 100\n"),
    ("INFILTRATION", "[INFILTRATION]\nS1 3.0 0.5 4.0\n"),
    ("LID_CONTROLS", "[LID_CONTROLS]\nBIOCELL SURFACE 1.0 0.5 0.1 1.0 0\n"),
    ("LID_USAGE", "[LID_USAGE]\nS1 BIOCELL 1 100 10 0 50 0\n"),
    ("AQUIFERS", "[AQUIFERS]\nAQ1 0.45 0.10 0.25 5.0 10.0 2.0 0.5 3.0 0.0 10.0\n"),
    ("GROUNDWATER", "[GROUNDWATER]\nS1 AQ1 J1 0 1 1 1 1 1 1\n"),
    ("SNOWPACKS", "[SNOWPACKS]\nSP1 PLOWABLE 0.1 0.2 0.3\n"),
    ("POLLUTANTS", "[POLLUTANTS]\nTSS MG/L\n"),
    ("LANDUSES", "[LANDUSES]\nRES 7 50 0\n"),
    ("BUILDUP", "[BUILDUP]\nRES TSS POWER 1.0 2.0 3.0 AREA\n"),
    ("WASHOFF", "[WASHOFF]\nRES TSS EXPON 1.0 2.0 50 0\n"),
    ("COVERAGES", "[COVERAGES]\nS1 RES 100\n"),
    ("TREATMENT", "[TREATMENT]\nJ1 TSS = 0.5 * FLOW\n"),
    ("INFLOWS", "[INFLOWS]\nJ1 FLOW TS1 FLOW 1.0 1.0 0.0 PAT1\n"),
    ("DWF", "[DWF]\nJ1 FLOW 1.0 PAT1 PAT2 PAT3 PAT4\n"),
    ("LOADINGS", "[LOADINGS]\nS1 TSS 5.0\n"),
    ("CURVES", "[CURVES]\nC1 STORAGE 0 0\n"),
    ("TIMESERIES", "[TIMESERIES]\nTS1 0:00 0.0 1:00 1.0\n"),
    ("PATTERNS", "[PATTERNS]\nPAT1 MONTHLY 1.0 1.0 1.0\n"),
    ("CONTROLS", "[CONTROLS]\nRULE R1 IF NODE J1 DEPTH > 1 THEN PUMP P1 STATUS = ON\n"),
    ("HYDROGRAPHS", "[HYDROGRAPHS]\nUH1 RG1\n"),
    ("RDII", "[RDII]\nJ1 UH1 10.0\n"),
    ("EVAPORATION", "[EVAPORATION]\nCONSTANT 0.1\n"),
    ("TEMPERATURE", "[TEMPERATURE]\nTIMESERIES TSTEMP\n"),
    ("MAP", "[MAP]\nDIMENSIONS 0 0 1000 1000\n"),
    ("COORDINATES", "[COORDINATES]\nJ1 100.0 200.0\n"),
    ("VERTICES", "[VERTICES]\nC1 110.0 210.0\n"),
    ("POLYGONS", "[POLYGONS]\nS1 0.0 0.0\n"),
    ("SYMBOLS", "[SYMBOLS]\nRG1 50.0 50.0\n"),
    ("LABELS", '[LABELS]\n100 200 "Main Basin"\n'),
    ("TAGS", "[TAGS]\nNODE J1 TAG_A\n"),
    ("BACKDROP", "[BACKDROP]\nFILE map.png\n"),
    ("PROFILE", "[PROFILE]\nLINK C1\n"),
]


@pytest.mark.parametrize("section_name, section_text", SECTION_CASES)
def test_lalr_each_section_parses(section_name, section_text):
    parser = Lark.open_from_package(
        "swmm.parse", "input-lalr.lark", ("grammars",), parser="lalr"
    )

    tree = parser.parse(section_text)

    assert tree is not None, f"{section_name} did not produce a parse tree"


def test_lalr_all_sections_together_parses():
    parser = Lark.open_from_package(
        "swmm.parse", "input-lalr.lark", ("grammars",), parser="lalr"
    )

    inp_text = "\n".join(text.strip() for _, text in SECTION_CASES) + "\n"

    tree = parser.parse(inp_text)

    assert tree is not None


EVAPORATION_CASES = [
    ("CONSTANT", "[EVAPORATION]\nCONSTANT 0.1\n"),
    ("MONTHLY", "[EVAPORATION]\nMONTHLY 1 1 1 1 1 1 1 1 1 1 1 1\n"),
    ("TIMESERIES", "[EVAPORATION]\nTIMESERIES TS1\n"),
    ("TEMPERATURE", "[EVAPORATION]\nTEMPERATURE\n"),
    ("FILE", "[EVAPORATION]\nFILE climate-evap.dat\n"),
    ("RECOVERY", "[EVAPORATION]\nRECOVERY PAT1\n"),
    ("DRY_ONLY", "[EVAPORATION]\nDRY_ONLY YES\n"),
]


@pytest.mark.parametrize("variant_name, section_text", EVAPORATION_CASES)
def test_evaporation_variants(variant_name, section_text):
    parser = Lark.open_from_package(
        "swmm.parse", "input-lalr.lark", ("grammars",), parser="lalr"
    )

    tree = parser.parse(section_text)

    assert tree is not None, f"EVAPORATION variant {variant_name} did not parse"

    # Optional stronger check: ensure variant keyword is present in tree string
    # (useful when debugging token retention issues)
    tree_s = str(tree)
    assert variant_name in tree_s, f"{variant_name} missing from parse tree output"
    print(tree_s)


def test_lalr():

    # Read expected tree from file
    with open(EXPECTED_TREE, "r") as file:
        expected = file.read().strip()

    # Convert input file to parse tree
    parser = Lark.open_from_package(
        "swmm.parse", "input-lalr.lark", ("grammars",), parser="lalr"
    )

    # Create parse tree and convert to string
    with open(EXAMPLE_PROJECT) as f:
        file_tree = parser.parse(f.read())

    output = str(file_tree).strip()

    # print(output)
    assert expected == output
