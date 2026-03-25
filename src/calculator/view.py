from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CalculatorView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aperture Science Quantum Number Cruncher")
        self.setMinimumSize(600, 500)  # Science doesn't fit in fixed boxes!

        # Cave Johnson mandated QSS stylesheet soup
        import os

        style_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Column for the actual calculator
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=2)

        # Branding
        branding = QLabel("APERTURE LABORATORIES\nQUANTUM CALCULATOR")
        branding.setObjectName("brandingLabel")
        branding.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(branding)

        # Display screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(self.display)

        # Grid for buttons
        grid_layout = QGridLayout()
        left_layout.addLayout(grid_layout)

        # Right Column for History Logs
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, stretch=1)

        history_label = QLabel("EXPERIMENTAL LOG:")
        right_layout.addWidget(history_label)

        self.history_table = QTableWidget(0, 2)
        self.history_table.horizontalHeader().setVisible(False)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(False)
        self.history_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.history_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        right_layout.addWidget(self.history_table)

        self.buttons = {}

        # Button matrix: (text, row, col, row_span, col_span)
        btn_map = [
            ("MC", 0, 0, 1, 1),
            ("MR", 0, 1, 1, 1),
            ("M+", 0, 2, 1, 1),
            ("(", 0, 3, 1, 1),
            (")", 0, 4, 1, 1),
            ("7", 1, 0, 1, 1),
            ("8", 1, 1, 1, 1),
            ("9", 1, 2, 1, 1),
            ("/", 1, 3, 1, 1),
            ("C", 1, 4, 1, 1),
            ("4", 2, 0, 1, 1),
            ("5", 2, 1, 1, 1),
            ("6", 2, 2, 1, 1),
            ("*", 2, 3, 1, 1),
            ("+", 2, 4, 1, 1),
            ("1", 3, 0, 1, 1),
            ("2", 3, 1, 1, 1),
            ("3", 3, 2, 1, 1),
            ("-", 3, 3, 1, 1),
            ("=", 3, 4, 2, 1),
            ("0", 4, 0, 1, 2),
            (".", 4, 2, 1, 1),
            ("√", 4, 3, 1, 1),
        ]

        for item in btn_map:
            text, row, col, row_span, col_span = item
            btn = QPushButton(text)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.buttons[text] = btn
            if text == "=":
                btn.setObjectName("btnCalculate")
            elif text == "C":
                btn.setObjectName("btnClear")
            grid_layout.addWidget(btn, row, col, row_span, col_span)

    def update_display(self, text: str):
        """Updates the text on the calculator screen."""
        self.display.setText(text)

    def update_history(self, history_list):
        """Updates the experimental logs on the side panel."""
        self.history_table.setRowCount(len(history_list))
        for row, (eq, ans) in enumerate(history_list):
            self.history_table.setItem(row, 0, QTableWidgetItem(eq))
            self.history_table.setItem(row, 1, QTableWidgetItem(f" = {ans}"))
        self.history_table.scrollToBottom()
