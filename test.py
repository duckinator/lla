#!/usr/bin/env python3

"""
1*1 = 1
1*0 = 0
1+1 = 1
1+0 = 1

character       ||  NEGATE_NEXT | IDENTIFIER | OPERATOR
================||=====================================
   !            ||    1         | 0          | 0
   &            ||    0         | 0          | 1
   |            ||    0         | 0          | 1
[a-zA-Z0-9.-]+
"""

from parser import parse
from tokenizer import OperatorType, TokenType


class Interpreter:
    """Very basic interpreter."""

    def __init__(self, code, variables):
        self.tree = parse(code)
        self.variables = variables
        self.result = None

    def _resolve(self, var):
        value = self.variables[var.value]
        if var.negated:
            value = not value
        return value

    def _run(self, current):
        if isinstance(current, bool):
            return current

        if hasattr(current, 'left'):
            current.left = self._run(current.left)

        if hasattr(current, 'right'):
            current.right = self._run(current.right)

        if current.type == TokenType.STATEMENT:
            return current.right
        if current.type == TokenType.IDENTIFIER:
            return self._resolve(current)
        if current.operator_type == OperatorType.AND:
            return current.left and current.right
        if current.operator_type == OperatorType.OR:
            return current.left or current.right

        print(f'WTF IS THIS?: {current!r}')
        raise Exception(':(')

    def run(self):
        """Executes the code, then returns `self` for method chaining."""
        self.result = self._run(self.tree)
        return self



def main():
    print(Interpreter('website_up & !search', {'website_up': True, 'search': False}).run().result)

    return

    programs = [
        '!website_up | (!search & (!elasticsearch.http | !elasticsearch.process))',
        '!website_up | !search & (!elasticsearch.http | !elasticsearch.process)',
        '!website_up & !search & ssh & search.local & elasticsearch.http & elasticsearch.process',
        '!website_up & !search & !ssh',
        '!website_up & !search & ssh & !elasticsearch.process',
        '!website_up & !search & ssh & !elasticsearch.http & elasticsearch.process',
        'website_up    &    !search',
    ]

    for program in programs:
        #parse_tree = parse(program)
        #print(parse_tree)
        Interpreter(program).run()


if __name__ == "__main__":
    main()
