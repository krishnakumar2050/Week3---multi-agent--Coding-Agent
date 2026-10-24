"""Behavior and security regression tests included in the review snapshot."""

import pytest
from vulnerable import average, calculate


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("-3 + +2", -1),
        ("7 / 2", 3.5),
        ("7 // 2", 3),
        ("7 % 2", 1),
        ("1.25 + 2.5", 3.75),
        (" 42 ", 42),
        ("0", 0),
        ("3 - 5", -2),
        ("-(2 + 3)", -5),
    ],
)
def test_supported_arithmetic(expression, expected):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "__import__('builtins')",
        "open('file')",
        "(1).__class__",
        "variable",
        "True",
        "'hello'",
        "[1, 2]",
        "1j",
        "2 ** 10",
        "1 << 2",
        "1 < 2",
        "lambda: 1",
        "1 if True else 2",
        "[x for x in []]",
        "(x := 1)",
        "",
        "2 +",
        "1; 2",
    ],
)
def test_rejects_unsupported_syntax(expression):
    with pytest.raises(ValueError):
        calculate(expression)


def test_rejected_expression_has_no_side_effect(tmp_path):
    target = tmp_path / "must-not-exist"
    expression = f"__import__('pathlib').Path({str(target)!r}).touch()"
    with pytest.raises(ValueError):
        calculate(expression)
    assert not target.exists()


@pytest.mark.parametrize("expression", ["1 / 0", "1 // 0", "1 % 0"])
def test_zero_divisor(expression):
    with pytest.raises(ZeroDivisionError):
        calculate(expression)


@pytest.mark.parametrize(
    "expression", ["1e309", "1e101", "1e100 * 10", "9" * 513, "+".join(["1"] * 50)]
)
def test_resource_and_numeric_limits(expression):
    with pytest.raises(ValueError):
        calculate(expression)


@pytest.mark.parametrize("expression", [None, 42, b"1+2"])
def test_expression_requires_string(expression):
    with pytest.raises(TypeError):
        calculate(expression)


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([2, 4], 3),
        ([7], 7),
        ([-4, -2], -3),
        ([1.5, 2.5], 2),
        ((0, 2), 1),
        ([0], 0),
        ([1e308, 1e308], 1e308),
    ],
)
def test_average(values, expected):
    assert average(values) == expected


@pytest.mark.parametrize("values", [[], ()])
def test_empty_average(values):
    with pytest.raises(ValueError, match="at least one"):
        average(values)


def test_average_rejects_nonnumeric_items():
    with pytest.raises(TypeError):
        average([1, "2"])


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1e100", 1e100),
        ("-1e100", -1e100),
        ("1" + " " * 511, 1),
        ("+".join(["1"] * 43), 43),
    ],
)
def test_valid_resource_boundaries(expression, expected):
    assert calculate(expression) == expected
