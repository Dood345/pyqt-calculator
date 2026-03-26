from unittest.mock import MagicMock

import pytest

from calculator.controller import CalculatorController
from calculator.model import CalculatorModel


@pytest.fixture
def mock_view():
    view = MagicMock()
    # Mock specific view components
    view.buttons = {
        "1": MagicMock(),
        "=": MagicMock(),
        "C": MagicMock(),
        "MC": MagicMock(),
        "MR": MagicMock(),
        "M+": MagicMock(),
        "√": MagicMock(),
        "^": MagicMock(),
        "C_hex": MagicMock(),
        "AND": MagicMock(),
        "HEX": MagicMock(),
    }
    view.history_table = MagicMock()
    view.btn_toggle_drawer = MagicMock()
    view.drawer_widget = MagicMock()
    view.radix_indicator = MagicMock()
    view.keyPressed = MagicMock()
    return view


@pytest.fixture
def model():
    return CalculatorModel()


@pytest.fixture
def controller(mock_view, model):
    return CalculatorController(mock_view, model)


def test_initialization_connects_signals(mock_view, controller):
    # Signals are mapped during init
    for btn in mock_view.buttons.values():
        btn.clicked.connect.assert_called()
    mock_view.history_table.itemClicked.connect.assert_called_with(
        controller._on_history_clicked
    )
    mock_view.btn_toggle_drawer.clicked.connect.assert_called_with(
        controller._on_toggle_drawer_clicked
    )
    mock_view.keyPressed.connect.assert_called_with(
        controller._handle_key_press
    )


def test_drawer_toggle(mock_view, controller):
    # False initially implies it transitions to True
    mock_view.drawer_widget.isVisible.return_value = False
    controller._on_toggle_drawer_clicked()

    mock_view.drawer_widget.setVisible.assert_called_with(True)
    mock_view.btn_toggle_drawer.setText.assert_called_with(">")

    # Transition to False
    mock_view.drawer_widget.isVisible.return_value = True
    controller._on_toggle_drawer_clicked()

    mock_view.drawer_widget.setVisible.assert_called_with(False)
    mock_view.btn_toggle_drawer.setText.assert_called_with("<")


def test_button_clicked_updates_model_and_view(mock_view, model, controller):
    controller._on_button_clicked("5")
    assert model.current_expression == "5"
    mock_view.update_display.assert_called_with("5")


def test_equal_clicked(mock_view, model, controller):
    model.current_expression = "5+5"
    controller._on_equal_clicked()
    mock_view.update_display.assert_called_with("10")
    mock_view.update_history.assert_called()
    assert model.current_expression == "10"


def test_clear_clicked(mock_view, model, controller):
    model.current_expression = "123"
    controller._on_clear_clicked()
    assert model.current_expression == ""
    mock_view.update_display.assert_called_with("")


def test_backspace_clicked(mock_view, model, controller):
    model.current_expression = "12"
    controller._on_backspace_clicked()
    assert model.current_expression == "1"
    mock_view.update_display.assert_called_with("1")


def test_sqrt_clicked(mock_view, model, controller):
    model.current_expression = "25"
    controller._on_sqrt_clicked()
    assert model.current_expression == "√(25)"
    mock_view.update_display.assert_called_with("√(25)")


def test_radix_clicked(mock_view, model, controller):
    model.current_expression = "10"
    controller._on_radix_clicked("HEX")
    assert model.radix_mode == "HEX"
    assert model.current_expression == "0xa"
    mock_view.radix_indicator.setText.assert_called_with("RADIX: HEX")
    mock_view.update_display.assert_called_with("0xa")


def test_history_clicked(mock_view, model, controller):
    mock_item = MagicMock()
    mock_item.text.return_value = " = 42"

    controller._on_history_clicked(mock_item)
    assert model.current_expression == "42"
    mock_view.update_display.assert_called_with("42")

    mock_item.text.return_value = "5+5"
    controller._on_history_clicked(mock_item)
    assert model.current_expression == "5+5"
    mock_view.update_display.assert_called_with("5+5")


def test_memory_buttons(mock_view, model, controller):
    # M+
    model.current_expression = "10"
    controller._on_m_plus_clicked()
    assert model.memory_val == 10.0

    # MR
    model.current_expression = "5+"
    controller._on_mr_clicked()
    assert model.current_expression == "5+10"
    mock_view.update_display.assert_called_with("5+10")

    # MC
    controller._on_mc_clicked()
    assert model.memory_val == 0.0


def test_handle_key_press(mock_view, model, controller):
    controller._handle_key_press("5")
    assert model.current_expression == "5"
    mock_view.update_display.assert_called_with("5")

    controller._handle_key_press("BACKSPACE")
    assert model.current_expression == ""

    controller._handle_key_press("CLEAR")
    assert model.current_expression == ""

    model.current_expression = "3*4"
    controller._handle_key_press("=")
    assert model.current_expression == "12"
