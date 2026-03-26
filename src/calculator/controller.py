class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        """Connects UI buttons to controller methods."""
        for value, button in self.view.buttons.items():
            button.clicked.connect(
                # had to add checked because PyQt buttons emit
                # a boolean when clicked, and we don't want
                # that getting mixed up with our values
                lambda checked, v=value: self._on_button_clicked(v)
            )

    def _on_button_clicked(self, value: str):
        """Passes the value to the model and updates the view."""
        if value == "C":
            new_expression = self.model.clear()
            self.view.update_display(new_expression)
            self.view.update_history("")
        elif value == "⌫":
            new_expression = self.model.backspace()
            self.view.update_display(new_expression)
        elif value == "=":
            history, new_expression = self.model.evaluate()
            self.view.update_history(history)
            self.view.update_display(new_expression)
        else:
            new_expression = self.model.append_value(value)
            self.view.update_display(new_expression)
