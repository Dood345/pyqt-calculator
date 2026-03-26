import re


class CalculatorModel:
    """The model for the calculator application.

    This class handles the logic of the calculator, including
    appending values, clearing the expression, and evaluating it.
    """

    def __init__(self) -> None:
        self.current_expression = ""
        self.history = ""

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
            self.history = "Security Error"
            self.current_expression = ""
            return self.history, self.current_expression

        try:
            # string is safe to eval, no code bombs
            result = str(
                eval(self.current_expression, {"__builtins__": {}}, {})
            )
            self.history = self.current_expression + " ="
            self.current_expression = result

        except SyntaxError:
            self.history = "Syntax Error"
            self.current_expression = ""
        except ArithmeticError:
            self.history = "Math Error"
            self.current_expression = ""
        except TypeError:
            self.history = "Type Error"
            self.current_expression = ""

        return self.history, self.current_expression
