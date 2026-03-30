from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculatorView(QMainWindow):
    """The main window for the calculator application.

    This class handles the creation and layout of all UI elements,
    including the displays and the button grid.
    """

    def __init__(self) -> None:
        """Initializes the calculator view."""
        super().__init__()
        self.setWindowTitle("PyQt Calculator Prototype")
        self.setFixedSize(300, 400)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # History screen
        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(200)
        self.history_list.setStyleSheet("""
            border: none;
            color: gray;
            font-size: 12px;
        """)
        main_layout.addWidget(self.history_list)

        # Main display screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("font-size: 24px;")
        main_layout.addWidget(self.display)

        # Button layout area
        self.buttons_layout = QGridLayout()
        main_layout.addLayout(self.buttons_layout)

        # A dictionary to store all buttons for easy access in the controller
        self.buttons: dict[str, QPushButton] = {}

        self._create_buttons()

    def _create_buttons(self) -> None:
        """Creates the grid of calculator buttons."""
        # fmt: off
        button_layout_map = {
            "7": (0, 0), "8": (0, 1), "9": (0, 2), "/": (0, 3), "C": (0, 4),
            "4": (1, 0), "5": (1, 1), "6": (1, 2), "*": (1, 3), "(": (1, 4),
            "1": (2, 0), "2": (2, 1), "3": (2, 2), "-": (2, 3), ")": (2, 4),
            "0": (3, 0), ".": (3, 1), "⌫": (3, 2), "+": (3, 3), "=": (3, 4),
        }

        # Constructing each button
        for btn_text, pos in button_layout_map.items():
            button = QPushButton(btn_text)
            button.setFixedSize(45, 45)
            # color coding for important buttons
            if btn_text == "C":
                button.setStyleSheet("background-color: red;")
            elif btn_text == "⌫":
                button.setStyleSheet("background-color: orange;")
            elif btn_text == "=":
                button.setStyleSheet("background-color: green;")
            self.buttons[btn_text] = button
            self.buttons_layout.addWidget(button, pos[0], pos[1])

    def update_display(self, text: str) -> None:
        """Updates the central text on the calculator screen.

        Args:
            text: The string to display.
        """
        self.display.setText(text)

    def add_history(self, text: str) -> None:
        """Adds a history item to the list and scrolls to bottom.

        Args:
            text: The string to display as history.
        """
        self.history_list.addItem(text)
        self.history_list.scrollToBottom()

    def clear_history(self) -> None:
        """Clears the history list."""
        self.history_list.clear()
