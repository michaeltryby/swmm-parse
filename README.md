# swmm-parse

File parsing toolkit for SWMM

## Build

Builds src and binary distributions

```
% python -m build
```

## Test

Installs requirements and runs tests

```
% pip install -r test-requirements.txt
% pytest
```

## Usage

Convert SWMM input into a parse tree.

```
from lark import Lark

l = Lark.open_from_package(
"swmm.parse", "input-earley.lark", ("grammars",), parser="earley"
)

input = """
[TITLE]
Hello SWMM!
"""

print(l.parse(input))
```

Output

```
Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'section'), [Token('KEYWORD', 'TITLE'), Tree(Token('RULE', 'record'), [Tree('keyword', [Token('KEYWORD', 'Hello')]), Tree('name', [Token('NAME', 'SWMM!')])])])])
```
