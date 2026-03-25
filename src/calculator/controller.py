class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        """Connects UI buttons to controller methods."""
        for text, btn in self.view.buttons.items():
            if text == "=":
                btn.clicked.connect(self._on_equal_clicked)
            elif text == "C":
                btn.clicked.connect(self._on_clear_clicked)
            elif text == "MC":
                btn.clicked.connect(self._on_mc_clicked)
            elif text == "MR":
                btn.clicked.connect(self._on_mr_clicked)
            elif text == "M+":
                btn.clicked.connect(self._on_m_plus_clicked)
            elif text == "√":
                btn.clicked.connect(self._on_sqrt_clicked)
            else:
                # Capture the text variable correctly in the lambda
                btn.clicked.connect(
                    lambda checked, t=text: self._on_button_clicked(t)
                )

        self.view.history_table.itemClicked.connect(self._on_history_clicked)

    def _on_history_clicked(self, item):
        """Loads a clicked history item back into the calculator display."""
        text = item.text()
        if text.startswith(" = "):
            val = text[3:]
            self.model.current_expression = val
            self.view.update_display(val)
        else:
            self.model.current_expression = text
            self.view.update_display(text)

    def _on_mc_clicked(self):
        self.model.memory_clear()

    def _on_mr_clicked(self):
        new_expr = self.model.memory_recall()
        self.view.update_display(new_expr)

    def _on_m_plus_clicked(self):
        self.model.memory_add()

    def _on_sqrt_clicked(self):
        new_expression = self.model.apply_sqrt()
        self.view.update_display(new_expression)

    def _on_button_clicked(self, value: str):
        """Passes the value to the model and updates the view."""
        new_expression = self.model.append_value(value)
        self.view.update_display(new_expression)

    def _on_equal_clicked(self):
        """Evaluates the expression."""
        result = self.model.calculate()
        self.view.update_display(result)
        self.view.update_history(self.model.history)

    def _on_clear_clicked(self):
        """Clears the expression."""
        cleared = self.model.clear()
        self.view.update_display(cleared)
