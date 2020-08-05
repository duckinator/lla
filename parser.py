from textwrap import indent

from tokenizer import TokenType, OperatorType


class Program:
    def __init__(self):
        self.right = None

    def __str__(self):
        return f"{self.right}"

    def __repr__(self):
        return f"<Program code={self.right!r}>"


class Parens:
    def __init__(self):
        self.right = None

    def __str__(self):
        return f'({self.right})'

    def __repr__(self):
        return f'Parens({self.right!r})'


class Operator:
    symbol = "UNKNOWN_OPERATOR"

    def __init__(self, left=None, operator=None, right=None):
        self.left = left
        self.right = right
        self.operator = operator

        self.type = TokenType.OPERATOR
        self.value = operator.value
        self.negated = operator.negated
        self.operator_type = operator.operator_type

    def __str__(self):
        return f"{str(self.left)} {self.symbol} {str(self.right)}"

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left!r}, {self.right!r})'


class And(Operator):
    symbol = '&'


class Or(Operator):
    symbol = '|'


def nest_parens(orig_tokens):
    """Given a list of tokens, put parenthesized sections into nested lists."""
    orig_tokens = orig_tokens.copy()
    tokens = []
    chunk = []
    in_chunk = False
    for token in orig_tokens:
        if token.operator_type == OperatorType.OPEN_PAREN:
            in_chunk = True
            continue

        if token.operator_type == OperatorType.CLOSE_PAREN:
            in_chunk = False
            tokens.append(chunk)
            chunk = []
            continue

        if in_chunk:
            chunk.append(token)
        else:
            tokens.append(token)
    return tokens


OPERATOR_MAP = {
    OperatorType.AND: And,
    OperatorType.OR: Or,
}


def parse(orig_tokens, toplevel_class=None):
    """Given a series of tokens, return a parse tree."""
    tokens = nest_parens(orig_tokens)

    #from pprint import pprint
    #pprint(tokens)

    if toplevel_class is None:
        toplevel_class = Program

    toplevel = toplevel_class()
    parent = toplevel
    while tokens:
        left = tokens.pop(0)
        operator = tokens.pop(0)

        if isinstance(left, list):
            left = parse(left, Parens)

        current = OPERATOR_MAP[operator.operator_type](left, operator)

        if len(tokens) == 1:
            right = tokens.pop(0)
            if isinstance(right, list):
                right = parse(right, Parens)
            current.right = right

        parent.right = current
        parent = current
    return toplevel
