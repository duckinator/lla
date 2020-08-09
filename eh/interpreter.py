"""
A very basic interpreter.
"""

from .parser import parse
from .tokenizer import OperatorType, TokenType


class UndefinedVariableException(Exception):
    """Exception raised when a variable couldn't be resolved."""
    def __init__(self, variable):
        super().__init__(f'Undefined variable: {variable}')


class Interpreter:  # pylint: disable=too-few-public-methods
    """Very basic interpreter."""

    def __init__(self, variables):
        self.variables = variables

    def _resolve(self, var):
        if not var.value in self.variables:
            raise UndefinedVariableException(var.value)

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

        raise Exception(f'Unhandled object: {current!r}')

    def run(self, code):
        """Executes the code, then returns the final boolean value."""
        tree = parse(code)
        return self._run(tree)
