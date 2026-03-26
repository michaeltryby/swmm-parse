#
#  to_input_file.py
#
#  Created: Apr 25, 2024
#  Updated: Mar 25, 2026
#
#  Author:  Michael E. Tryby
#           US EPA - ORD/CESER
#

from lark import Token, Tree, Visitor

NL = "\n"
SP = " "
NS = ""


class ToInputFile(Visitor):
    def __init__(self):
        self._buffer = []

    def export(self):
        return NS.join(self._buffer)

    @staticmethod
    def _is_header_token(tok):
        return isinstance(tok, Token) and tok.type.endswith("_HEADER")

    @staticmethod
    def _is_newline_token(tok):
        return isinstance(tok, Token) and (
            tok.type in {"_NL", "NEWLINE"} or tok.value == "\n"
        )

    def _flatten_tokens(self, node):
        out = []

        def walk(obj):
            if isinstance(obj, Token):
                out.append(obj)
            elif isinstance(obj, Tree):
                for ch in obj.children:
                    walk(ch)

        walk(node)
        return out

    def __default__(self, tree):
        first = tree.children[0] if tree.children else None

        # Section: first child is a _HEADER token
        if isinstance(first, Token) and self._is_header_token(first):
            if self._buffer:
                self._buffer.append(NL)
            self._buffer.append(first.value)
            self._buffer.append(NL)
            return

        # Record nodes: *_rec
        if str(tree.data).endswith("_rec"):
            fields = [
                tok.value
                for tok in self._flatten_tokens(tree)
                if not self._is_newline_token(tok) and not self._is_header_token(tok)
            ]

            if fields:
                self._buffer.append(SP.join(fields))
                self._buffer.append(NL)
