import re


class CalculatorModel:
    """The model for the calculator application.

    This class handles the logic of the calculator, including
    appending values, clearing the expression, and evaluating it.
    """

    def __init__(self) -> None:
        self.current_expression = ""
        self.history: list[str] = []

    def append_value(self, value: str) -> str:
        """Appends a value and returns the new expression."""
        self.current_expression += value
        return self.current_expression

    def clear(self) -> str:
        """Clears the current expression."""
        self.current_expression = ""
        return self.current_expression

    def backspace(self) -> str:
        """Removes the last character from the expression."""
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
        return self.current_expression

    def evaluate(self) -> tuple[str, str]:
        """Evaluates the expression and returns history and result."""
        # only allow numbers, hex/bin/oct, and math operators
        # moved away from stack data structure due to python's eval()
        pattern = (
            r"(?:0[xX][0-9a-fA-F]+"
            r"|0[bB][01]+"
            r"|0[oO][0-7]+"
            r"|[\d]+\.?\d*"
            r"|[\+\-\*\/\(\)\.])*"
        )
        if not re.fullmatch(pattern, self.current_expression):
            history_item = "Security Error"
            self.history.append(history_item)
            self.current_expression = ""
            return history_item, self.current_expression

        try:
            # string is safe to eval, no code bombs
            result = str(
                eval(self.current_expression, {"__builtins__": {}}, {})
            )
            history_item = f"{self.current_expression} = {result}"
            self.history.append(history_item)
            self.current_expression = result

        except SyntaxError:
            history_item = "Syntax Error"
            self.history.append(history_item)
            self.current_expression = ""
        except ArithmeticError:
            history_item = "Math Error"
            self.history.append(history_item)
            self.current_expression = ""
        except TypeError:
            history_item = "Type Error"
            self.history.append(history_item)
            self.current_expression = ""

        return history_item, self.current_expression
