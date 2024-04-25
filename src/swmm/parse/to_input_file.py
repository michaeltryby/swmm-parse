#
#  to_input_file.py
#
#  Created: Dec  7, 2023
#  Updated: Apr 23, 2024
#
#  Author:  Michael E. Tryby
#           US EPA - ORD/CESER
#

import sys

from lark import Visitor


NL = '\n'
SP = ' '


class ToInputFile(Visitor):
# Writes file parse tree to input file
    def __init__(self):
        self.buffer = []

    def export(self):
        print(''.join(self.buffer), end='')

    def section(self, tree):
        self.buffer.append(NL)
        self.buffer.append(f"[{tree.children[0]}]" + NL)

    def record(self, tree):
        fields = [sub_tree.children[0] for sub_tree in tree.children]
        line = ' '.join(fields) + NL
        self.buffer.append(line)
