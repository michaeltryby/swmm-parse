#
#  to_input_file.py
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
    def _token_value(obj):
        if isinstance(obj, Token):
            return obj.value
        return str(obj)

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
                return
            if isinstance(obj, Tree):
                for ch in obj.children:
                    walk(ch)
                return

        walk(node)
        return out

    def __default__(self, tree):
        data = str(tree.data)

        # Section nodes: *_sec
        if data.endswith("_sec"):
            if self._buffer:
                self._buffer.append(NL)

            header = None
            for tok in self._flatten_tokens(tree):
                v = self._token_value(tok)
                if v.startswith("[") and v.endswith("]"):
                    header = v
                    break

            if header is None:
                # fallback only
                header = f"[{data[:-4].upper()}]"

            self._buffer.append(header)
            self._buffer.append(NL)
            return

        # Record nodes: *_rec
        if data.endswith("_rec"):
            fields = []
            for tok in self._flatten_tokens(tree):
                if self._is_newline_token(tok):
                    continue
                fields.append(self._token_value(tok))

            if fields:
                self._buffer.append(SP.join(fields))
                self._buffer.append(NL)
            return
