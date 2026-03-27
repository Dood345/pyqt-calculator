from PyQt6.QtCore import Qt

from calculator.controller import CalculatorController
from calculator.model import CalculatorModel
from calculator.view import CalculatorView


def test_controller_initialization(qtbot):
    view = CalculatorView()
    model = CalculatorModel()
    controller = CalculatorController(view, model)
    qtbot.addWidget(view)

    assert controller.view is view
    assert controller.model is model


def test_button_append(qtbot):
    view = CalculatorView()
    model = CalculatorModel()
    # disabling unused variable error for flake8
    controller = CalculatorController(view, model)  # noqa: F841
    qtbot.addWidget(view)

    # Click '7' button
    qtbot.mouseClick(view.buttons["7"], Qt.MouseButton.LeftButton)
    assert model.current_expression == "7"
    assert view.display.text() == "7"


def test_button_clear(qtbot):
    view = CalculatorView()
    model = CalculatorModel()
    # disabling unused variable error for flake8
    controller = CalculatorController(view, model)  # noqa: F841
    qtbot.addWidget(view)

    model.append_value("85")
    qtbot.mouseClick(view.buttons["C"], Qt.MouseButton.LeftButton)
    assert model.current_expression == ""
    assert view.display.text() == ""
    assert view.history_list.count() == 0


def test_button_backspace(qtbot):
    view = CalculatorView()
    model = CalculatorModel()
    # disabling unused variable error for flake8
    controller = CalculatorController(view, model)  # noqa: F841
    qtbot.addWidget(view)

    qtbot.mouseClick(view.buttons["9"], Qt.MouseButton.LeftButton)
    qtbot.mouseClick(view.buttons["⌫"], Qt.MouseButton.LeftButton)
    assert model.current_expression == ""
    assert view.display.text() == ""


def test_button_evaluate(qtbot):
    view = CalculatorView()
    model = CalculatorModel()
    # disabling unused variable error for flake8
    controller = CalculatorController(view, model)  # noqa: F841
    qtbot.addWidget(view)

    model.current_expression = "2+2"
    qtbot.mouseClick(view.buttons["="], Qt.MouseButton.LeftButton)
    assert view.display.text() == "4"
    assert view.history_list.item(0).text() == "2+2 = 4"
