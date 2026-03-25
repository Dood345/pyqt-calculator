class CalculatorModel:
    def __init__(self):
        self.current_expression = ""

    def append_value(self, value: str) -> str:
        """Appends a value and returns the new expression."""
        self.current_expression = self.current_expression + value
        return self.current_expression
