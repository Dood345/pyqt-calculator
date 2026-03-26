import pytest

from calculator.model import CalculatorModel


@pytest.fixture
def model():
    return CalculatorModel()


def test_initial_state(model):
    assert model.current_expression == ""
    assert model.history == []
    assert model.memory_val == 0.0
    assert model.radix_mode == "DEC"


def test_append_value(model):
    model.append_value("5")
    assert model.current_expression == "5"
    model.append_value("+")
    assert model.current_expression == "5+"


def test_clear_expression(model):
    model.append_value("5+5")
    model.clear()
    assert model.current_expression == ""


def test_remove_last_char(model):
    model.append_value("123")
    assert model.remove_last_char() == "12"
    assert model.current_expression == "12"
    assert model.remove_last_char() == "1"
    assert model.remove_last_char() == ""
    assert model.remove_last_char() == ""


def test_memory_operations(model):
    # Add to memory when blank
    model.memory_add()
    assert model.memory_val == 0.0

    # Calculate and store
    model.current_expression = "5+5"
    model.memory_add()
    assert model.memory_val == 10.0

    # Add again to memory
    model.current_expression = "10"
    model.memory_add()
    assert model.memory_val == 20.0

    # Clear memory
    model.memory_clear()
    assert model.memory_val == 0.0

    # Recall memory
    model.memory_val = 42.0
    model.current_expression = "1+"
    model.memory_recall()
    assert model.current_expression == "1+42"

    # Float recall
    model.memory_val = 42.5
    model.current_expression = ""
    model.memory_recall()
    assert model.current_expression == "42.5"


def test_apply_sqrt(model):
    # Empty
    assert model.apply_sqrt() == ""

    # Simple number
    model.current_expression = "16"
    assert model.apply_sqrt() == "√(16)"

    # Preceded by operator
    model.current_expression = "5+16"
    assert model.apply_sqrt() == "5+√(16)"

    # Preceded by operator but no number
    model.current_expression = "5+"
    assert model.apply_sqrt() == "5+√(5)"

    # Nested or with parens
    model.current_expression = "5+(16)"
    assert model.apply_sqrt() == "5+(√(16))"


def test_change_radix(model):
    model.current_expression = "10"
    assert model.change_radix("HEX") == "0xa"
    assert model.radix_mode == "HEX"

    model.current_expression = "0xa"
    assert model.change_radix("BIN") == "0b1010"

    model.current_expression = "0b1010"
    assert model.change_radix("OCT") == "0o12"

    model.current_expression = "0o12"
    assert model.change_radix("DEC") == "10"

    # Float converts gracefully or doesn't change
    model.current_expression = "10.5"
    assert model.change_radix("HEX") == "0xa"  # int(10.5) => 10 => 0xa


def test_calculate_basic_math(model):
    model.current_expression = "5+3"
    assert model.calculate() == "8"
    assert model.history == [("5+3", "8")]

    model.current_expression = "10-4"
    assert model.calculate() == "6"

    model.current_expression = "6*7"
    assert model.calculate() == "42"

    model.current_expression = "8/2"
    assert model.calculate() == "4"


def test_calculate_precedence(model):
    model.current_expression = "2+3*4"
    assert model.calculate() == "14"

    model.current_expression = "(2+3)*4"
    assert model.calculate() == "20"

    model.current_expression = "10-2*3+4"
    assert model.calculate() == "8"


def test_calculate_exponent_associativity(model):
    # 2^3^2 -> 2^(3^2) -> 2^9 -> 512
    model.current_expression = "2^3^2"
    assert model.calculate() == "512"

    # Mixed with other operators
    model.current_expression = "2*3^2"
    assert model.calculate() == "18"


def test_calculate_unary_minus(model):
    model.current_expression = "-5+10"
    assert model.calculate() == "5"

    model.current_expression = "5+(-3)"
    assert model.calculate() == "2"


def test_calculate_bitwise(model):
    model.current_expression = "10&2"
    assert model.calculate() == "2"

    model.current_expression = "10|2"
    assert model.calculate() == "10"

    model.current_expression = "10⊕2"  # XOR
    assert model.calculate() == "8"

    model.current_expression = "1<<3"
    assert model.calculate() == "8"

    model.current_expression = "8>>2"
    assert model.calculate() == "2"


def test_calculate_sqrt(model):
    model.current_expression = "√(16)"
    assert model.calculate() == "4"

    model.current_expression = "2*√(9)"
    assert model.calculate() == "6"

    # Imaginary lie
    model.current_expression = "√(-1)"
    assert model.calculate() == "Error: Anomalous Materials"


def test_calculate_errors(model):
    model.current_expression = "5/0"
    assert model.calculate() == "Error: Cake is a lie"

    model.current_expression = "5+*"
    assert model.calculate() == "Error: Anomalous Materials"


def test_calculate_mixed_radix(model):
    model.current_expression = "0xa+0b10"  # 10 + 2
    assert model.calculate() == "12"

    model.radix_mode = "HEX"
    model.current_expression = "10+2"
    assert model.calculate() == "0xc"
