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
        self.referenced_variables = set()
        self.last_referenced_variable = None

    def _resolve(self, var):
        self.referenced_variables.add(var.value)
        self.last_referenced_variable = var.value
        if not var.value in self.variables:
            raise UndefinedVariableException(var.value)

        value = self.variables[var.value]
        if var.negated:
            value = not value
        return value

    def _run(self, current):
        if isinstance(current, bool):
            return current

        if current.type == TokenType.STATEMENT:
            return self._run(current.right)
        if current.type == TokenType.IDENTIFIER:
            return self._resolve(current)
        if current.operator_type == OperatorType.AND:
            return self._run(current.left) and self._run(current.right)
        if current.operator_type == OperatorType.OR:
            return self._run(current.left) or self._run(current.right)

        raise Exception(f'Unhandled object: {current!r}')

    def run(self, code):
        """Executes the code, then returns the final boolean value."""
        tree = parse(code)
        return self._run(tree)
