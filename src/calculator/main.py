import sys

from controller import CalculatorController
from model import CalculatorModel
from PyQt6.QtWidgets import QApplication
from view import CalculatorView


def main():
    app = QApplication(sys.argv)

    view = CalculatorView()
    model = CalculatorModel()

    CalculatorController(view, model)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
