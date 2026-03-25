class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        """Connects UI buttons to controller methods."""
        # When btn_seven is clicked, run self._on_button_clicked
        self.view.btn_seven.clicked.connect(
            lambda: self._on_button_clicked("7")
        )

    def _on_button_clicked(self, value: str):
        """Passes the value to the model and updates the view."""
        new_expression = self.model.append_value(value)
        self.view.update_display(new_expression)
