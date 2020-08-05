from textwrap import indent

from tokenizer import TokenType, OperatorType


class Program:
    def __init__(self):
        self.right = None

    def __str__(self):
        return f"{self.right}"

    def __repr__(self):
        return f"<Program code={str(self)!r}>"


class Parens:
    def __init__(self):
        self.left = None
        self.right = None

    def __str__(self):
        return f'({self.right})'



class Operator:
    def __init__(self, operator, right):
        self.left = None
        self.right = right
        self.operator = operator

        self.type = TokenType.OPERATOR
        self.value = operator.value
        self.negated = operator.negated
        self.operator_type = operator.operator_type

    def __str__(self):
        return f"{str(self.left)} {self.__class__.__name__.upper()} {str(self.right)}"


class And(Operator):
    pass


class Or(Operator):
    pass


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

    if toplevel_class is None:
        toplevel_class = Program

    toplevel = toplevel_class()
    last = None
    while tokens:
        if last is None:
            last = toplevel
            left, *tokens = tokens
        else:
            left = None
        operator, right, *tokens = tokens

        if isinstance(right, list):
            right = parse(right, Parens)

        current = OPERATOR_MAP[operator.operator_type](operator, right)

        if left:
            current.left = left

        last.right = current
        last = current
    return toplevel
