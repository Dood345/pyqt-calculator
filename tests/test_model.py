from calculator.model import CalculatorModel


def test_model_initial_state():
    model = CalculatorModel()
    assert model.current_expression == ""
    assert model.history == []


def test_append_value():
    model = CalculatorModel()
    model.append_value("1")
    assert model.append_value("+") == "1+"
    assert model.current_expression == "1+"


def test_clear():
    model = CalculatorModel()
    model.append_value("123")
    assert model.clear() == ""
    assert model.current_expression == ""


def test_backspace():
    model = CalculatorModel()
    # Empty backspace
    assert model.backspace() == ""

    # Backspace with content
    model.append_value("42")
    assert model.backspace() == "4"
    assert model.backspace() == ""
    assert model.backspace() == ""


def test_evaluate_success():
    model = CalculatorModel()
    model.append_value("3+4")
    history, expr = model.evaluate()
    assert history == "3+4 = 7"
    assert expr == "7"


def test_evaluate_security_error():
    model = CalculatorModel()
    model.current_expression = "import os"
    history, expr = model.evaluate()
    assert history == "Security Error"
    assert expr == ""


def test_evaluate_syntax_error():
    model = CalculatorModel()
    model.current_expression = "+*"
    history, expr = model.evaluate()
    assert history == "Syntax Error"
    assert expr == ""


def test_evaluate_math_error():
    model = CalculatorModel()
    model.current_expression = "1/0"
    history, expr = model.evaluate()
    assert history == "Math Error"
    assert expr == ""


def test_evaluate_type_error():
    model = CalculatorModel()
    model.current_expression = "1+()"  # Causes TypeError without SyntaxWarning
    history, expr = model.evaluate()
    assert history == "Type Error"
    assert expr == ""
