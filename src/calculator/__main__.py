import sys

from PyQt6.QtWidgets import QApplication

from calculator.controller import CalculatorController
from calculator.model import CalculatorModel
from calculator.view import CalculatorView


def main() -> None:
    """The main entry point for the calculator application."""
    app = QApplication(sys.argv)

    view = CalculatorView()
    model = CalculatorModel()

    CalculatorController(view, model)

    view.show()
    sys.exit(app.exec())


main()
