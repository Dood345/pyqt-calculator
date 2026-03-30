import sys  # pragma: no cover

from PyQt6.QtWidgets import QApplication  # pragma: no cover

from calculator.controller import CalculatorController  # pragma: no cover
from calculator.model import CalculatorModel  # pragma: no cover
from calculator.view import CalculatorView  # pragma: no cover


def main() -> None:  # pragma: no cover
    """
    The main entry point for the calculator application.
    """

    app = QApplication(sys.argv)

    view = CalculatorView()
    model = CalculatorModel()

    CalculatorController(view, model)

    view.show()
    sys.exit(app.exec())


"""
Entry point guard, prevents running this file as a script
This little if statement is a security checkpoint.
It asks: "Are we running this file directly? If yes,
fire up the main() sequence and start the application!
"""
if __name__ == "__main__":  # pragma: no cover
    main()
