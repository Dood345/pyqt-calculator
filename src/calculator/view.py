from PyQt6.QtWidgets import (
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculatorView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Calculator Prototype")
        self.setFixedSize(300, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Display screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display)

        # A single button to test the wiring
        self.btn_seven = QPushButton("7")
        layout.addWidget(self.btn_seven)

    def update_display(self, text: str):
        """Updates the text on the calculator screen."""
        self.display.setText(text)
