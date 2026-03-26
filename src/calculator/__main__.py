import sys  # pragma: no cover

from PyQt6.QtWidgets import QApplication  # pragma: no cover

from calculator.controller import CalculatorController  # pragma: no cover
from calculator.model import CalculatorModel  # pragma: no cover
from calculator.view import CalculatorView  # pragma: no cover


def main() -> None:  # pragma: no cover
    """The main entry point for the calculator application."""
    app = QApplication(sys.argv)

    view = CalculatorView()
    model = CalculatorModel()

    CalculatorController(view, model)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
