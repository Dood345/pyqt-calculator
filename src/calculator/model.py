import math
import re


class CalculatorModel:
    def __init__(self):
        self.current_expression = ""
        self.history = []
        self.memory_val = 0.0
        self.radix_mode = "DEC"

    def apply_sqrt(self) -> str:
        """
        Wraps the current number in sqrt(). If the expression ends with
        an operator, it appends sqrt() of the preceding number instead.
        """
        expr = self.current_expression
        if not expr:
            return expr

        m_op = re.search(r"([+\-*/\s]+)$", expr)
        if m_op:
            tail = m_op.group(1)
            body = expr[: -len(tail)]
            if not body:
                return expr

            m_num = re.search(r"(\d+(?:\.\d+)?)(\)*)$", body)
            if m_num:
                num_str = m_num.group(1)
                self.current_expression = f"{expr}√({num_str})"
            else:
                self.current_expression = f"{expr}√({body})"
        else:
            body = expr
            m_num = re.search(r"(\d+(?:\.\d+)?)(\)*)$", body)
            if m_num:
                num_str = m_num.group(1)
                closing_parens = m_num.group(2)
                prefix = body[: -(len(num_str) + len(closing_parens))]
                self.current_expression = (
                    f"{prefix}√({num_str}){closing_parens}"
                )
            else:
                self.current_expression = f"√({body})"

        return self.current_expression

    def append_value(self, value: str) -> str:
        """Appends a value and returns the new expression."""
        self.current_expression = self.current_expression + value
        return self.current_expression

    def change_radix(self, new_mode: str) -> str:
        """Changes the radix mode and reformats the current value."""
        self.radix_mode = new_mode
        if not self.current_expression:
            return ""

        try:
            tokens = re.findall(
                r"^0x[0-9a-fA-F]+$|^0b[01]+$|^0o[0-7]+$|^\d+\.\d+$|^\d+$",
                self.current_expression.strip(),
            )
            if tokens:
                val = tokens[0]
                if (
                    val.startswith("0x")
                    or val.startswith("0b")
                    or val.startswith("0o")
                ):
                    num = float(int(val, 0))
                else:
                    num = float(val)

                if new_mode == "HEX":
                    self.current_expression = hex(int(num))
                elif new_mode == "BIN":
                    self.current_expression = bin(int(num))
                elif new_mode == "OCT":
                    self.current_expression = oct(int(num))
                else:
                    self.current_expression = (
                        str(int(num)) if num.is_integer() else str(num)
                    )
        except Exception:
            pass

        return self.current_expression

    def clear(self) -> str:
        """Clears the current expression."""
        self.current_expression = ""
        return self.current_expression

    def memory_add(self):
        """Adds current evaluated result to memory."""
        try:
            val = float(self.calculate()) if self.current_expression else 0.0
            self.memory_val += val
        except Exception:
            pass

    def memory_clear(self):
        """Clears the memory bank."""
        self.memory_val = 0.0

    def memory_recall(self) -> str:
        """Retrieves memory value and appends to the current expression."""
        val_str = (
            str(int(self.memory_val))
            if self.memory_val.is_integer()
            else str(self.memory_val)
        )
        self.current_expression += val_str
        return self.current_expression

    def _precedence(self, op):
        if op == "√":
            return 6
        if op in ("*", "/"):
            return 5
        if op in ("+", "-"):
            return 4
        if op in ("<<", ">>"):
            return 3
        if op == "&":
            return 2
        if op == "^":
            return 1
        if op == "|":
            return 0
        return -1

    def _apply_operator(self, operators, values):
        op = operators.pop()
        if op == "√":
            right = values.pop()
            if right < 0:
                raise ValueError("Imaginary numbers are a lie")
            values.append(math.sqrt(right))
            return

        right = values.pop()
        left = values.pop()
        if op == "+":
            values.append(left + right)
        elif op == "-":
            values.append(left - right)
        elif op == "*":
            values.append(left * right)
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError("Cake is a lie")
            values.append(left / right)
        elif op == "&":
            values.append(int(left) & int(right))
        elif op == "|":
            values.append(int(left) | int(right))
        elif op == "^":
            values.append(int(left) ^ int(right))
        elif op == "<<":
            values.append(int(left) << int(right))
        elif op == ">>":
            values.append(int(left) >> int(right))

    def calculate(self) -> str:
        """Evaluates the mathematical expression using PEMDAS Stack Parsing"""
        if not self.current_expression:
            return ""

        original_expr = self.current_expression
        expr = self.current_expression.replace(" ", "")

        # Handle simple unary minus safely
        if expr.startswith("-"):
            expr = "0" + expr
        expr = expr.replace("(-", "(0-")

        try:
            # Tokenize floats, ints, operators
            tokens = re.findall(
                r"0x[0-9a-fA-F]+|0b[01]+|0o[0-7]+|[a-fA-F]|"
                r"\d+\.\d+|\d+|<<|>>|[+\-*/()&|^√]",
                expr,
            )
            values = []
            operators = []

            for token in tokens:
                if (
                    token.startswith("0x")
                    or token.startswith("0b")
                    or token.startswith("0o")
                ):
                    values.append(float(int(token, 0)))
                elif token.replace(".", "", 1).isdigit():
                    values.append(float(token))
                elif token in ("(", "√"):
                    operators.append(token)
                elif token == ")":
                    while operators and operators[-1] != "(":
                        self._apply_operator(operators, values)
                    if operators:
                        operators.pop()  # pop '('
                elif token in ("+", "-", "*", "/", "<<", ">>", "&", "|", "^"):
                    while (
                        operators
                        and operators[-1] != "("
                        and self._precedence(operators[-1])
                        >= self._precedence(token)
                    ):
                        self._apply_operator(operators, values)
                    operators.append(token)

            while operators:
                self._apply_operator(operators, values)

            if len(values) == 1:
                res = values[0]
                if self.radix_mode == "HEX":
                    result_str = hex(int(res))
                elif self.radix_mode == "BIN":
                    result_str = bin(int(res))
                elif self.radix_mode == "OCT":
                    result_str = oct(int(res))
                else:
                    result_str = str(int(res)) if res.is_integer() else str(res)

                self.history.append((original_expr, result_str))
                self.current_expression = result_str
                return result_str
            else:
                raise Exception("Missing operators")
        except ZeroDivisionError:
            self.current_expression = ""
            return "Error: Cake is a lie"
        except Exception:
            self.current_expression = ""
            return "Error: Anomalous Materials"
