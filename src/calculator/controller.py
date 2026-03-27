from calculator.model import CalculatorModel
from calculator.view import CalculatorView


class CalculatorController:
    """The controller for the calculator application.

    This class handles the logic of the calculator, including
    appending values, clearing the expression, and evaluating it.
    """

    def __init__(self, view: CalculatorView, model: CalculatorModel) -> None:
        self.view = view
        self.model = model
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connects UI buttons to controller methods."""
        for value, button in self.view.buttons.items():
            button.clicked.connect(
                # had to add checked because PyQt buttons emit
                # a boolean when clicked, and we don't want
                # that getting mixed up with our values
                lambda checked, v=value: self._on_button_clicked(v)
            )
        self.view.history_list.itemClicked.connect(self._on_history_clicked)

    def _on_history_clicked(self, item) -> None:
        """Handles clicks on history items by appending their equations."""
        text = item.text()
        if "=" in text:
            equation = text.split("=")[0].strip()
            new_expression = self.model.append_value(equation)
            self.view.update_display(new_expression)

    def _on_button_clicked(self, value: str) -> None:
        """Passes the value to the model and updates the view."""
        # too simple to need handlers
        if value == "C":
            new_expression = self.model.clear()
            self.view.update_display(new_expression)
            self.view.clear_history()
        elif value == "⌫":
            new_expression = self.model.backspace()
            self.view.update_display(new_expression)
        elif value == "=":
            history, new_expression = self.model.evaluate()
            self.view.add_history(history)
            self.view.update_display(new_expression)
        else:
            new_expression = self.model.append_value(value)
            self.view.update_display(new_expression)
