from textwrap import indent

from tokenizer import TokenType, OperatorType


class Program:
    def __init__(self):
        self.right = None

    def __str__(self):
        return f'{self.right}'

    def __repr__(self):
        return f'<Program code={self.right!r}>'


class Parens:
    def __init__(self):
        self.right = None

    def __str__(self):
        return f'({self.right})'

    def __repr__(self):
        return f'Parens({self.right!r})'


class Operator:
    symbol = 'UNKNOWN_OPERATOR'

    def __init__(self, left=None, operator=None, right=None):
        self.left = left
        self.right = right
        self.operator = operator

        self.type = TokenType.OPERATOR
        self.value = operator.value
        self.negated = operator.negated
        self.operator_type = operator.operator_type

    def __str__(self):
        return f'{str(self.left)} {self.symbol} {str(self.right)}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left!r}, {self.right!r})'


class And(Operator):
    symbol = '&'


class Or(Operator):
    symbol = '|'


def _nest_parens(orig_tokens):
    """Main logic of nest_parens()."""
    orig_tokens = orig_tokens.copy()
    tokens = []
    while orig_tokens:
        token = orig_tokens.pop(0)
        not_list = not isinstance(token, list)
        if not_list and token.operator_type == OperatorType.OPEN_PAREN:
            chunk, orig_tokens = _nest_parens(orig_tokens)
            tokens.append(chunk)
        elif not_list and token.operator_type == OperatorType.CLOSE_PAREN:
            return (tokens, orig_tokens)
        else:
            tokens.append(token)
    return (tokens, orig_tokens)


def nest_parens(orig_tokens):
    """Given a sequence of tokens, put parenthesized sections into nested lists."""
    tokens, remaining = _nest_parens(orig_tokens)
    if len(remaining) > 0:
        raise Exception(f'Excess tokens: {", ".join(map(repr, remaining))}')
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
