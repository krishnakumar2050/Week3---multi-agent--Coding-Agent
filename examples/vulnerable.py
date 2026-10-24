"""Small arithmetic helpers with explicit validation and no code evaluation."""

import ast
import math
import operator
from statistics import mean

_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression):
    """Evaluate finite numeric literals with +, -, *, /, //, %, and parentheses.

    Unary + and - are supported. Names, calls, attributes, booleans, strings,
    collections, and exponentiation are rejected with ValueError. Expressions
    are limited to 512 characters and 128 AST nodes; numeric literals and
    intermediate results must be finite and at most 1e100 in magnitude.
    Division or modulo by zero raises ZeroDivisionError.
    """
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    if len(expression) > 512:
        raise ValueError("expression exceeds 512 characters")
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except (SyntaxError, RecursionError) as exc:
        raise ValueError("invalid arithmetic expression") from exc
    if sum(1 for _ in ast.walk(tree)) > 128:
        raise ValueError("expression exceeds 128 syntax nodes")

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            result = node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            result = _BINARY[type(node.op)](evaluate(node.left), evaluate(node.right))
        elif isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            result = _UNARY[type(node.op)](evaluate(node.operand))
        else:
            raise ValueError("only numeric literals and supported arithmetic operators are allowed")
        if abs(result) > 1e100 or not math.isfinite(result):
            raise ValueError("numeric value must be finite and at most 1e100 in magnitude")
        return result

    return evaluate(tree.body)


def average(values):
    """Return the arithmetic mean of a nonempty, sized numeric sequence.

    Empty sequences raise ValueError. Nonnumeric items raise TypeError.
    """
    if len(values) == 0:
        raise ValueError("average requires at least one value")
    return mean(values)
