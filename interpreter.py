"""
A very basic interpreter.
"""

from parser import parse
from tokenizer import OperatorType, TokenType


class Interpreter:  # pylint: disable=too-few-public-methods
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

        raise Exception(f'Un-handled object: {current!r}')

    def run(self):
        """Executes the code, then returns `self` for method chaining."""
        self.result = self._run(self.tree)
        return self
